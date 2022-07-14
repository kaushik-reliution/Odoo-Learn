from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StudentAdmission(models.Model):
    _name = "student.admission"
    student_id = fields.Many2one('student.record', String="Admission")
    a_seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                        default=lambda self: _('New'))
    date_adm = fields.Date(string="Date of Admission")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, tracking=True)
    std = fields.Integer(string="Standard")
    mobile = fields.Integer(string="Mobile No.", required=True)

    def action_submit(self):
        return True

    @api.onchange('student_id')
    def onchange_student_id(self):
        if self.student_id.id:
            if self.student_id.gender:
                self.gender = self.student_id.gender
                if self.student_id.std:
                    self.std = self.student_id.std
            else:
                self.gender = ''
                self.std = ''
