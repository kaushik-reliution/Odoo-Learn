from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _description = "Order Line"
    _inherit = "crm.lead"
    warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse Id")
    crm_line_ids = fields.One2many('crm.lead.line', 'crm_id', string="Product Details")
    # sale_order_count = fields.Integer(string="Orders", compute='_compute_sale_data')
    is_won = fields.Boolean(related='stage_id.is_won', string="Is Won")

    # def _compute_sale_data(self):
    #     for lead in self:
    #         total = 0.0
    #         quotation_cnt = 0
    #         sale_order_cnt = 0
    #         company_currency = lead.company_currency or self.env.company.currency_id
    #         for order in lead.order_ids:
    #             if order.state in ('draft', 'sent'):
    #                 quotation_cnt += 1
    #             if order.state not in ('draft', 'sent', 'cancel'):
    #                 sale_order_cnt += 1
    #                 total += order.currency_id._convert(
    #                     order.amount_untaxed, company_currency, order.company_id,
    #                     order.date_order or fields.Date.today())
    #         lead.sale_amount_total = total
    #         lead.quotation_count = quotation_cnt
    #         lead.sale_order_count = sale_order_cnt


    # Not required at this time(Sale order smart button action)
    # def action_view_crm_to_sale_order(self):
    #     action = self.env["ir.actions.actions"]._for_xml_id("sale.action_orders")
    #     # action['context'] = {
    #     #     'search_default_partner_id': self.partner_id.id,
    #     #     'default_partner_id': self.partner_id.id,
    #     #     'default_opportunity_id': self.id,
    #     # }
    #     # action['domain'] = [('opportunity_id', '=', self.id), ('state', 'not in', ('draft', 'sent', 'cancel'))]
    #     orders = self.mapped('order_ids').filtered(lambda l: l.state not in ('draft', 'sent', 'cancel'))
    #     if len(orders) == 1:
    #         action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
    #         action['res_id'] = orders.id
    #     return action

    def action_new_order_line(self):
        if not self.partner_id:
            raise ValidationError("Required Partner Id")
        if not self.crm_line_ids:
            raise ValidationError("At least 1 line required")
        sale_line_ids = []
        for line in self.crm_line_ids:
            sale_line_ids.append((0, 0, {'product_id': line.product_id.id, 'price_unit': line.product_id.lst_price,
                                         'name': line.name, 'product_uom_qty': line.quantity}))
        sales = {
                'opportunity_id': self.id,
                'partner_id': self.partner_id.id or '',
                'campaign_id': self.campaign_id.id,
                'medium_id': self.medium_id.id,
                'origin': self.name,
                'source_id':  self.source_id.id,
                'company_id': self.company_id.id or self.env.company.id,
                'tag_ids': [(6, 0, self.tag_ids.ids)],
                'order_line': sale_line_ids,
            }# other info lines in sale.order page
        self.env['sale.order'].create(sales)


    # """
    # Crone Method
    # """
    # def _sale_order_automation(self):
    #     crm = self.search([('stage_id.is_won', '=', True)])
    #     # sale = self.env['sale.order']
    #     for lead_id in crm:
    #         lead_id.action_new_order_line()

class CrmLeadLine(models.Model):
    _name = "crm.lead.line"
    _description = "Product Details"
    crm_id = fields.Many2one('crm.lead')
    product_id = fields.Many2one('product.product', string="Product")
    name = fields.Text('Description')
    quantity = fields.Float("Quantity", default=1.0)
    # qty = fields.Many2one('production.packaging', string="Quantity")
    qty_available = fields.Float(related='product_id.qty_available', string="OnHand Quantity")
    uom_id = fields.Many2one('uom.uom', string="Unit Of Measure")
    price_unit = fields.Float(related='product_id.lst_price', string="Unit Price")
    tax_ids = fields.Many2many('account.tax', string="Taxes")

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id.description_sale:
            raise ValidationError("123")
        else:
            self.name = self.product_id.name




