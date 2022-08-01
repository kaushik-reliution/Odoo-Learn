from odoo import models
import logging

_logger = logging.getLogger("<<<<<<<< Credit Limit Management >>>>>>>>")


class SaleOrder(models.Model):
    """
    Task[2813]: Customer Credit Limit Management
    Working hierarchy: action_confirm return wizard view and check credit limit of customer whether it is exceed or not....
    """
    _inherit = 'sale.order'

    def action_confirm(self):
        if self.partner_id.credit_limit:
            account_move_obj = self.env['account.move']
            s_order = self.env['sale.order'].search([('state', '=', 'sale'), ('partner_id', '=', self.partner_id.id),
                                                     ('invoice_status', '=', 'no')])
            total_used_amt = self.amount_total
            for partner_id in s_order.partner_invoice_id + self.partner_id:
                invoices, credit_notes = account_move_obj.get_credit_limit_invoices(partner_id)
                total_used_amt += account_move_obj.total_used_amt(partner_id, invoices, credit_notes)
            _logger.info(f"Total Used Amount :------>>> {total_used_amt}",
                         f"Customer Credit Limit :----->>{self.partner_id.credit_limit_amount}"
                         f"sale orders:<><><><>{s_order.ids}")
            if total_used_amt > self.partner_id.credit_limit_amount:
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'credit.limit.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                }
        return super(SaleOrder, self).action_confirm()
