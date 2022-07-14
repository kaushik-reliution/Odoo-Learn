from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    """
    Task[2813]: Customer Credit Limit Management
    Working hierarchy: action_confirm return wizard view and check credit limit exceed or not....
    """
    _inherit = ['sale.order']
    override_credit_limit = fields.Boolean(String="Override Credit Limit")
    temp_credit = fields.Float()  # temporary field to store credit limit

    def unpaid_amt(self):
        amt = 0
        so_obj = self.env['sale.order'].search([('partner_id', '=', self.partner_id.id), ('state', '=', 'sale'),
                                                ('invoice_status', '!=', 'invoiced')])
        inv = self.env['account.move'].search(
            [('move_type', '=', 'out_invoice'), ('partner_id', '=', so_obj.partner_id.id),
             ('payment_state', '=', 'not_paid')])
        notes = self.env['account.move'].search([('move_type', '=', 'out_refund'),
                                                 ('partner_id', '=', so_obj.partner_id.id),
                                                 ('payment_state', '=', 'not_paid'), ('state', '=', 'posted')])
        for record in inv:
            amt = amt + record.amount_residual
        for rec in so_obj:
            amt = amt + rec.amount_total
        amt_new = amt - notes.amount_residual
        return amt_new

    def action_confirm(self):
        if self.partner_id.active_credit_limit is True:
            if self.partner_id.warning_amt > 0:
                if self.partner_id.warning_amt > self.unpaid_amt():
                    if self.override_credit_limit is False:
                        return {
                            'type': 'ir.actions.act_window',
                            'res_model': 'credit.limit.wizard',
                            'view_mode': 'form',
                            'target': 'new',
                        }
        return super(SaleOrder, self).action_confirm()

    @api.onchange('override_credit_limit')
    def onchange_credit(self):
        if self.override_credit_limit is True:
            self.partner_id.warning_amt = self.unpaid_amt()



