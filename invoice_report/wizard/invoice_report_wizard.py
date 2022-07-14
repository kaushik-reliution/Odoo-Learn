import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class InvoiceReportWizard(models.TransientModel):
    _name = 'invoice.report.wizard'
    partner_id = fields.Many2one('res.partner', string='Customer')
    date_from = fields.Date(string="From Date")
    date_to = fields.Date(string="Date to")

    def report_data(self):
        record = {}
        date_from = self.date_from
        date_to = self.date_to
        record.update({
            'date_from': date_from,
            'date_to': date_to,
        })
        invoice_ids = self.env['account.move'].search([('state', '=', 'posted')])
        if invoice_ids:
            for invoices in invoice_ids:
                record['invoice'] = invoice_ids
                record['invoices'] = {}
                record['invoices']['invoice_date'] = invoices.invoice_date
                print("hellllll",  invoices.invoice_date)
            return record

    def inv_print_report(self):
        return self.env.ref('invoice_report.action_invoice_summary_report').report_action(self)

    def send_invoice_report(self):
        template_id = self.env.ref('invoice_report.emai_invoice_summary').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

