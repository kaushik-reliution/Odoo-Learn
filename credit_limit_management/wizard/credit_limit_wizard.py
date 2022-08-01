from werkzeug.urls import url_encode
import logging
from odoo import fields, models

_logger = logging.getLogger("<<<<<<<< Credit Limit Management >>>>>>>>")


class CreditLimitWizard(models.TransientModel):
    """
    Task(2813): Credit Limit Management
    Working hierarchy: @param: pending_invoices_line_ids"[Many2many]" receives all pending invoices with its existing
    fields... and set its value using default_get to wizard...
    """
    _name = "credit.limit.wizard"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin', 'ir.mail_server']
    partner_id = fields.Many2one('res.partner', string="Customer")
    credit_limit = fields.Float(related='partner_id.credit_limit_amount', string="Credit Limit")
    available_amount_due = fields.Float(string="Total Amount Due")
    total_used_amount = fields.Float(string="Total Amount Used")
    current_sale_order_amount = fields.Float(string="Order Amount")
    pending_invoices_line_ids = fields.Many2many('account.move', 'move_rel', 'move_id', 'move_name',
                                                 string="Pending Invoices")
    sale_order_ids = fields.Many2many('sale.order', string="Sale Orders")
    credit_notes = fields.Many2many('account.move', 'move_rel', 'move_id', 'move_name', string="Credit Notes")
    email_to = fields.Char()
    name = fields.Char()
    team_id = fields.Char()
    user_id = fields.Char()
    email_from = fields.Char()

    def default_get(self, fields):
        rec = super(CreditLimitWizard, self).default_get(fields)
        res_id = self.env.context.get('active_id')
        order = self.env['sale.order'].browse(res_id)
        usr_id = order.team_id.user_id
        smtp_server = self.env['ir.mail_server'].search([('active', '=', True)])
        rec['email_to'] = usr_id.email
        rec['name'] = order.name
        rec['team_id'] = usr_id.name
        rec['user_id'] = usr_id.name
        rec['email_from'] = smtp_server.smtp_user

        if res_id:
            amt = 0
            credit_amount = 0
            so_obj = self.env['sale.order'].browse(res_id)
            inv_obj = self.env['account.move'].search([('move_type', '=', 'out_invoice'),
                                                       ('partner_id', '=', so_obj.partner_invoice_id.id),
                                                       ('payment_state', '=', 'not_paid'), ('state', '=', 'posted')])
            _logger.info(f"Invoice Ids:======== {inv_obj}")
            notes = self.env['account.move'].search([('move_type', '=', 'out_refund'),
                                                     ('partner_id', '=', so_obj.partner_invoice_id.id),
                                                     ('payment_state', '=', 'not_paid'), ('state', '=', 'posted')])
            _logger.info(f"Credit Notes Ids<><><><><> {notes}")
            for vc in inv_obj:
                amt = amt + vc.amount_residual
            _logger.info(f"Pending Invoices Amount:--->>>> {amt}")
            for not_amt in notes:
                credit_amount = credit_amount + not_amt.amount_residual
            _logger.info(f"Credit Note Amount(Total)!!!!::::: >> {credit_amount}")
            available_amount_due = amt - credit_amount
            total_used_amount = so_obj.amount_total + available_amount_due
            rec.update({
                'partner_id': so_obj.partner_id.id,
                'pending_invoices_line_ids': [(6, 0, inv_obj.ids)],
                'credit_notes': [(6, 0, notes.ids)],
                'total_used_amount': total_used_amount,
                'available_amount_due': available_amount_due,
                'current_sale_order_amount': so_obj.amount_total,
            })
        return rec

    def action_send_mail(self):
        template_id = self.env.ref('credit_limit_management.email_template_credit').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    def get_full_url(self):
        """
        Send mail with current sale order clickable link to manager or sales-person to inform
        credit limit of current customer...
        """
        self.ensure_one()
        res_id = self.env.context.get('active_id')
        order_id = self.env['sale.order'].browse(res_id)
        base_url = self.get_base_url()
        print(base_url)
        url_params = {
            'id': order_id.id,
            'view_type': 'form',
            'model': 'sale.order',
            'action': self.env.ref('sale.action_quotations_with_onboarding').id,
        }
        params = '/web?#%s' % url_encode(url_params)
        return base_url + params
