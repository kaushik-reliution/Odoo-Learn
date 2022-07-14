# from odoo import api, fields, models, _
# from odoo.exceptions import ValidationError
#
#
# class SaleOrder(models.Model):
#     """
#     Task[2813]: Customer Credit Limit Management
#     Working hierarchy: action_confirm return wizard view and check credit limit exceed or not....
#     """
#     _inherit = ['sale.order']
#     override_credit_limit = fields.Boolean(String="Override Credit Limit")
#     temp_credit = fields.Float()  # temporary field to store credit limit
#
#     def unpaid_amt(self):
#         amt = 0
#         so_obj = self.env['sale.order'].search([('partner_id', '=', self.partner_id.id), ('state', '=', 'sale'),
#                                                 ('invoice_status', '=', 'no')])
#         inv = self.env['account.move'].search(
#             [('move_type', '=', 'out_invoice'), ('partner_id', '=', so_obj.partner_id.id),
#              ('payment_state', '=', 'not_paid')])
#         for record in inv:
#             amt = amt + record.amount_residual
#         for rec in so_obj:
#             amt = amt + rec.amount_total
#             print(amt)
#         amt_new = amt + self.amount_total
#         return amt_new
#
#     def action_confirm(self):
#         if self.partner_id.active_credit_limit is True:
#             if self.partner_id.warning_amt > 0:
#                 if self.partner_id.warning_amt < self.unpaid_amt():
#                     if self.unpaid_amt() > self.partner_id.blocking_amt:
#                         return {
#                             'type': 'ir.actions.act_window',
#                             'res_model': 'credit.limit.wizard',
#                             'view_mode': 'form',
#                             'target': 'new',
#                         }
#                     else:
#                         raise ValidationError("Warning Amount must be smaller than Blocking Amount")
#             return super(SaleOrder, self).action_confirm()
#
#     @api.onchange('override_credit_limit')
#     def onchange_credit(self):
#         if self.unpaid_amt()>self.partner_id.blocking_amt:
#             raise ValidationError("125")
