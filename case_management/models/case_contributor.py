from odoo import api, fields, models, _
from datetime import datetime


class CaseContributor(models.Model):
    _name = 'case.contributor'
    _rec_name = "case_id"

    receipt_no = fields.Char(string='Receipt No', required=True, copy=False, default='New')
    contributor_id = fields.Many2one('res.partner')
    case_id = fields.Many2one('case.case', string="Case Id")
    contribution_amount = fields.Float(string="Contribution Amount")
    contribution_by = fields.Selection([('cash', "Cash"), ('bank', "Bank")])
    contribution_ref = fields.Char(string="Contribution Reference")
    contribution_received = fields.Boolean(string="is received")
    remark = fields.Char(string="Remark")
    # current_date = fields.datetime()
    date_now = datetime.now().strftime('%d-%m-%Y')

    @api.model
    def create(self, vals):
        if vals.get('receipt_no', 'New') == 'New':
            vals['receipt_no'] = self.env['ir.sequence'].next_by_code('case.contributor') or 'New'

        return super(CaseContributor, self).create(vals)

