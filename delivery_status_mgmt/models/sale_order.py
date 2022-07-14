from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):

    _inherit = ['sale.order']

    delivery_status = fields.Selection([

        ('nothing', 'Nothing To Deliver'),
        ('delivered', 'Delivered'),
        ('partially', 'Partially Delivered'),
        ], string='Delivery Status', compute='_compute_delivery_status', store=True)

    @api.depends('order_line.qty_delivered')
    def _compute_delivery_status(self):
        del_qty = 0
        order_qty = 0
        for line in self.order_line:
            order_qty = order_qty + line.product_uom_qty
            del_qty = del_qty + line.qty_delivered
        if del_qty == 0:
            self.delivery_status = 'nothing'
        elif del_qty == order_qty:
            self.delivery_status = 'delivered'
        else:
            self.delivery_status = 'partially'

    def action_print(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.report',
            'view_mode': 'form',
            'target': 'new',
        }

