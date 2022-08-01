import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class InvoiceReportWizard(models.TransientModel):
    _name = 'invoice.report.wizard'
    partner_id = fields.Many2one('res.partner', string='Customer')
    date_from = fields.Date(string="From Date")
    date_to = fields.Date(string="Date to")
    email_to = fields.Char()
    email_from = fields.Char()

    def report_data(self):
        record = {}
        smtp_server = self.env['ir.mail_server'].search([('active', '=', True)])
        res_id = self.env.context.get('active_id')
        order = self.env['sale.order'].browse(res_id)
        date_from = self.date_from
        date_to = self.date_to
        email_to = order.team_id.user_id.email
        email_from = smtp_server.smtp_user
        record.update({
            'date_from': date_from,
            'date_to': date_to,
            'email_to': email_to,
            'email_from': email_from,
        })
        domain = [('state', '=', 'posted'), ('move_type', '=', 'out_invoice')]
        if record.get('date_from'):
            domain.append(('invoice_date', '>=', record.get('date_from')))
        if record.get('date_to'):
            domain.append(('invoice_date', '<=', record.get('date_to')))
        invoice_ids = self.env['account.move'].search(domain)

        if invoice_ids:
            record['invoice'] = {}
            for invoice in invoice_ids:
                if invoice.partner_id.name in record['invoice'].keys():
                    vals = {
                        'name': invoice.name,
                        'date': invoice.invoice_date.strftime('%d %B, %Y'),
                        'amount': invoice.amount_total
                    }
                    record['invoice'][invoice.partner_id.name].append(vals)
                else:
                    record['invoice'][invoice.partner_id.name] = []
                    vals = {
                        'name': invoice.name,
                        'date': invoice.invoice_date.strftime('%d %B, %Y'),
                        'amount': invoice.amount_total
                    }
                    record['invoice'][invoice.partner_id.name].append(vals)
            print(record)
            return record

    def inv_print_report(self):
        return self.env.ref('invoice_report.action_invoice_summary_report').report_action(self)

    def send_invoice_report(self):
        template_id = self.env.ref('invoice_report.email_invoice_summary').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
