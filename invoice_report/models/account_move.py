from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = ['account.move']

    def action_invoice_report(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'invoice_report_wizard',
            'view_mode': 'form',
            'target': 'new',
        }

