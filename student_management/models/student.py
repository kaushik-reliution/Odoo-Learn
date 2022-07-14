from datetime import date

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date, datetime


class StudentManagement(models.Model):
    _name = "student.record"
    name = fields.Char(string="Student  Name", required=True)
    age = fields.Char(string="Age", compute='_compute_age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], required=True, default='male', tracking=True)
    city = fields.Char(string="City")
    state = fields.Selection([('draft', 'Draft'), ('process', 'In Process'),
                             ('done', 'Done'), ('cancel', 'Cancel')], string="Status")
    seq = fields.Char(string="Order Sequence", required=True, copy=False, readonly=True,
                      default=lambda self: _('New'))
    std = fields.Integer(string="Standard", required=True)
    b_date = fields.Date(string="Birth Date")

    def action_process(self):
        self.state = 'process'

    def action_done(self):
        self.state= 'done'

    @api.depends('age')
    def _compute_age(self):
        today = date.today()
        if self.b_date:
            self.age = today.year - self.b_date.year
        else:
            self.age = 0

    @api.model
    def create(self, val):
        if val.get('seq', _('New')) == _('New'):
            val['seq'] = self.env['ir.sequence'].next_by_code('student.record') or _('New')
        res = super(StudentManagement, self).create(val)
        return res

