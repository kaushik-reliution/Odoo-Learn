from odoo import api, fields, models, _


class CaseContributor(models.Model):
    _name = 'case.contributor'

    contributor_id = fields.Many2one('res.partner')
    case_id = fields.Many2one('case.case', string="Case Id")
    contribution_amount = fields.Float(string="Contribution Amount")
    contribution_by = fields.Selection([('cash', "Cash"), ('bank', "Bank")])
    contribution_ref = fields.Char(string="Contribution Reference")
    contribution_received = fields.Boolean(string="is received")

    # entry_form_ids = fields.One2many('entry.form', 'case_id', required=True)

    # @api.model
    # def create(self, vals):
    #     if vals.get('ref', 'New') == 'New':
    #         vals['ref'] = self.env['ir.sequence'].next_by_code('case.contributor') or 'New'
    #     return super(CaseContributor, self).create(vals)


