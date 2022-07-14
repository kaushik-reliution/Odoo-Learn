import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
_logger = logging.getLogger("<<<<<<<< sale order report >>>>>>>>")

class SaleOrderReport(models.TransientModel):
    _name = 'sale.order.report'
    _inherit = ['mail.thread']
    partner_id = fields.Many2one('res.partner', string='Customer')
    date_from = fields.Date(string="From Date")
    date_to = fields.Date(string="Date to")
    order_line_ids = fields.Many2many('sale.order.line')

    def so_print_report(self):
        data = {'date_from': self.date_from, 'date_to': self.date_to,
                'partner_id': self.partner_id.name, 'order_line_ids': self.order_line_ids
                }
        return self.env.ref('delivery_status_mgmt.action_sale_order_report').report_action(self, data=data)

    def send_report(self):
        template_id = self.env.ref('delivery_status_mgmt.email_template_sale').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    @api.onchange('partner_id')
    def onchange_lines(self):
        # _logger.info(f"partner id:------ {self.partner_id.id}")
        if self.partner_id:
            lines = self.env['sale.order.line'].search([('order_id.partner_id', '=', self.partner_id.id)])
            _logger.info(f"Order lines:------ {lines}, partner id:------ {self.partner_id.id}")
            self.order_line_ids = [(6, 0, lines.ids)]


class SaleOrderReportPdf(models.AbstractModel):
    _name = 'report.delivery_status_mgmt.sale_report_inherit'

    def _get_report_values(self, docids, data=None):
        domain = []
        if data.get('partner_id'):
            domain.append(('partner_id', '=', data.get('partner_id')))
        if data.get('date_from'):
            domain.append(('date_order', '>=', data.get('date_from')))
        if data.get('date_to'):
            domain.append(('date_order', '<=', data.get('date_to')))
        docs = self.env['sale.order'].search(domain)
        # order_line_ids = self.env['sale.order.line'].browse(data.get('order_line_ids'))
        # data.update({'order_line_ids': self.order_line_ids.name})
        print(docs)
        print(data)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'sale.order.report',
            'docs': docs,
            'datas': data,
        }
