from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AdmissionWizard(models.TransientModel):
    _name = "admission.wizard"
    student_id = fields.Many2one('student.record', String="Admission")
    f_name = fields.Char(string="Father's Name")
    m_name = fields.Char(string="Mother's Name")
    address = fields.Char(string="Address")
    mobile = fields.Integer(string="Mobile No:")
    update = fields.Boolean(string="Update Mobile ")
    stream_selection = fields.Selection([
        ('sci', 'Science'),
        ('comm', 'Commerce'),
        ('art', 'Arts')])
    std = fields.Integer(related='student_id.std')

    def action_admission_save(self):
        if self.update is True:
            self.env['student.admission'].browse(self._context.get('active_ids')).update({'mobile': self.mobile})
        else:
            raise ValidationError("To update mobile number please check update field")



