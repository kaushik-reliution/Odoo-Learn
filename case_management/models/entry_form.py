from odoo import api, fields, models, _


class EntryForm(models.Model):
    _name = 'entry.form'
    _rec_name = "entry_no"

    entry_id = fields.Many2one('case.case')
    entry_no = fields.Char(string="Entry No")
    entry_date = fields.Date(string="Entry Date")
    entry_close_date = fields.Date(string="Entry Close Date")
    is_completed = fields.Boolean(strin="Is Completed")

