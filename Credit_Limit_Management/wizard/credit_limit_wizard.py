from werkzeug.urls import url_encode

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo import Command
from odoo.addons.base.models.ir_mail_server import MailDeliveryException


class CreditLimitWizard(models.TransientModel):
    """
    Task(2813): Credit Limit Management
    Working hierarchy: @param: pending_invoices_line_ids"[Many2many]" receives all pending invoices with its existing
    fields... and set its value using default_get to wizard...
    """
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    # _inherit = 'mail.compose.message'
    _name = "credit.limit.wizard"
    partner_id = fields.Many2one('res.partner', string="Customer")
    credit_limit = fields.Float(related='partner_id.warning_amt', string="Credit Limit")
    unpaid_amt = fields.Float(string="Unpaid Amount")
    order_amt = fields.Float(string="Order Amount")
    exceed_amt = fields.Float(string="Exceed")
    pending_invoices_line_ids = fields.Many2many('account.move', 'move_rel', 'move_id', 'move_name',
                                                 string="Pending Invoices")
    sale_order_ids = fields.Many2many('sale.order', string="Sale Orders")
    credit_notes = fields.Many2many('account.move', 'move_rel', 'move_id', 'move_name', string="Credit Notes")
    email_to = fields.Char()
    name = fields.Char()
    team_id = fields.Char()
    user_id= fields.Char()

    def default_get(self, fields):
        rec = super(CreditLimitWizard, self).default_get(fields)
        res_id = self.env.context.get('active_id')
        order = self.env['sale.order'].browse(res_id)
        email_to = order.team_id.user_id.email
        rec['email_to'] = email_to
        rec['name'] = order.name
        rec['team_id'] = order.team_id.user_id.name
        rec['user_id'] = order.team_id.user_id

        if res_id:
            so_obj = self.env['sale.order'].browse(res_id)
            sal = self.env['sale.order'].search([('partner_id', '=', so_obj.partner_id.id), ('state', '=', 'sale'),
                                                 ('invoice_status', '=', 'no')])

            inv_obj = self.env['account.move'].search([('move_type', '=', 'out_invoice'),
                                                       ('partner_id', '=', so_obj.partner_id.id),
                                                       ('payment_state', '=', 'not_paid'), ('state', '=', 'posted')])
            notes = self.env['account.move'].search([('move_type', '=', 'out_refund'),
                                                     ('partner_id', '=', so_obj.partner_id.id),
                                                     ('payment_state', '=', 'not_paid'), ('state', '=', 'posted')])
            amt = 0

            credit = so_obj.partner_id.warning_amt
            for vc in inv_obj:
                amt = amt + vc.amount_residual #invoices total
            for order in sal:
                amt = amt + order.amount_total #invoice total + saleorder total
            unpaid_new = amt - notes.amount_residual
            exceed_amt = abs(unpaid_new + so_obj.amount_total - credit)
            rec['partner_id'] = so_obj.partner_id.id
            rec['pending_invoices_line_ids'] = [(6, 0, inv_obj.ids)]
            rec['sale_order_ids'] = [(6, 0, sal.ids)]
            rec['credit_notes'] = [(6, 0, notes.ids)]
            rec['exceed_amt'] = exceed_amt
            rec['unpaid_amt'] = unpaid_new
            rec['order_amt'] = so_obj.amount_total
        return rec

    def action_send_mail(self):
        # base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        # base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
        template_id = self.env.ref('Credit_Limit_Management.email_template_credit').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    def get_full_url(self):
        self.ensure_one()
        res_id = self.env.context.get('active_id')
        order_id = self.env['sale.order'].browse(res_id)
        base_url = self.env["ir.config_parameter"].get_param("web.base.url")
        url_params = {
            'id': order_id.id,
            'view_type': 'form',
            'model': 'sale.order',
            'action': self.env.ref('sale.action_quotations_with_onboarding').id,
        }
        params = '/web?#%s' % url_encode(url_params)
        return base_url + params

