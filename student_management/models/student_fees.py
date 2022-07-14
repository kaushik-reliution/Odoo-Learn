from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StudentFees(models.Model):
    _name = 'student.fees'
    student_id = fields.Many2one('student.record', String="Admission")
    tuition_fees = fields.Integer(string="Tuition Fees")
    adm_fees = fields.Integer(string='Admission Fees')
    lib_fees = fields.Integer(string="Library Fees")







