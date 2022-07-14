# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class VatReport(models.TransientModel):
    _name = 'vat.report'

    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')

    def calculate_vat(self):
        record = {}
        date_from = self.date_from
        date_to = self.date_to
        record.update({
            'date_from': date_from,
            'date_to': date_to
        })

        invoice_ids = self.env['account.move'].search(
            [('company_id', '=', self.env.company.id), ('invoice_date', '>=', date_from), ('state', '=', 'posted'),
             ('move_type', 'in', ['out_invoice', 'out_refund']), ('invoice_date', '<=', date_to)], order='invoice_date')
        record['invoice'] = {}
        inv_tax_total = 0
        inv_amount_total = 0
        inv_untaxed_amount_total = 0
        record['invoice']['inv_tax_total'] = inv_tax_total
        record['invoice']['inv_amount_total'] = inv_amount_total
        record['invoice']['inv_untaxed_amount_total'] = inv_untaxed_amount_total
        if invoice_ids:
            for inv in invoice_ids.invoice_line_ids:
                if inv.l10n_ae_vat_amount > 0:
                    if inv.move_id.move_type == 'out_invoice':
                        inv_tax_total += inv.l10n_ae_vat_amount
                        inv_amount_total += (inv.price_total - inv.l10n_ae_vat_amount)
                    if inv.move_id.move_type == 'out_refund':
                        inv_tax_total -= inv.l10n_ae_vat_amount
                        inv_amount_total -= (inv.price_total - inv.l10n_ae_vat_amount)
                else:
                    if inv.move_id.move_type == 'out_invoice':
                        inv_untaxed_amount_total += inv.price_total
                    if inv.move_id.move_type == 'out_refund':
                        inv_untaxed_amount_total -= inv.price_total
            record['invoice']['inv_tax_total'] = round(inv_tax_total, 2)
            record['invoice']['inv_amount_total'] = round(inv_amount_total, 2)
            record['invoice']['inv_untaxed_amount_total'] = round(inv_untaxed_amount_total, 2)

        bill_ids = self.env['account.move'].search(
            [('company_id', '=', self.env.company.id), ('invoice_date', '>=', date_from),
             ('invoice_date', '<=', date_to), ('state', '=', 'posted'),
             ('move_type', 'in', ['in_invoice', 'in_refund'])], order='invoice_date')
        record['bill'] = {}
        bill_tax_total = 0
        bill_amount_total = 0
        record['bill']['bill_tax_total'] = bill_tax_total
        record['bill']['bill_amount_total'] = bill_amount_total
        if bill_ids:
            for bill in bill_ids.invoice_line_ids:
                if bill.l10n_ae_vat_amount > 0:
                    if bill.move_id.move_type == 'in_invoice':
                        bill_tax_total += bill.l10n_ae_vat_amount
                        bill_amount_total += (bill.price_total - bill.l10n_ae_vat_amount)
                    if bill.move_id.move_type == 'in_refund':
                        bill_tax_total -= bill.l10n_ae_vat_amount
                        bill_amount_total -= (bill.price_total - bill.l10n_ae_vat_amount)
            record['bill']['bill_tax_total'] = round(bill_tax_total, 2)
            record['bill']['bill_amount_total'] = round(bill_amount_total, 2)

        expense_ids = self.env['hr.expense.sheet'].search(
            [('company_id', '=', self.env.company.id), ('accounting_date', '>=', date_from),
             ('accounting_date', '<=', date_to), ('state', 'in', ['post', 'done'])], order='accounting_date')
        record['exp'] = {}
        exp_tax_total = 0
        exp_amount_total = 0
        record['exp']['exp_tax_total'] = exp_tax_total
        record['exp']['exp_amount_total'] = exp_amount_total
        for line in expense_ids.account_move_id.line_ids:
            if line.parent_state == 'posted':
                if line.tax_line_id:
                    exp_tax_total += line.debit
                    exp_amount_total += line.tax_base_amount
        record['exp']['exp_tax_total'] = round(exp_tax_total, 2)
        record['exp']['exp_amount_total'] = round(exp_amount_total, 2)
        return record

    def print_report(self):
        return self.env.ref('vat_report.action_vat_report').report_action(self)
