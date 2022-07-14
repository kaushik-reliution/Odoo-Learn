from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CaseCase(models.Model):
    """
    Task [2994] Case Management for NGO
    """
    _name = 'case.case'
    _rec_name = "case_no"

    case_no = fields.Char(string='Case No', required=True, copy=False, readonly=True, default='New')
    case_start_date = fields.Date(string="Case Start Date", required=True)
    case_end_date = fields.Date(string="Case End Date", required=True)
    case_estimated_amount = fields.Float("Case Estimated Amount", required=True)
    case_achieved_amount = fields.Float("Case Received Amount", compute='_get_received_amount')
    case_remain_amount = fields.Float("Case Remaining Amount")
    contributor_ids = fields.One2many('case.contributor', 'case_id')
    entry_form_ids = fields.One2many('entry.form', 'entry_id')

    @api.model
    def create(self, vals):
        if vals.get('case_no', 'New') == 'New':
            vals['case_no'] = self.env['ir.sequence'].next_by_code('case.case') or 'New'
        return super(CaseCase, self).create(vals)

    @api.depends('contributor_ids.contribution_amount')
    def _get_received_amount(self):
        for rec in self:
            remain_amount = 0
            for amount in rec.contributor_ids:
                remain_amount = remain_amount + amount.contribution_amount
            rec.case_achieved_amount = remain_amount
            rec.case_remain_amount = rec.case_estimated_amount - rec.case_achieved_amount


