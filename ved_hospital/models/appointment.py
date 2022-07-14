from odoo import api, fields, models, _


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'reference'
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    rel_age = fields.Integer(string='Age', related='patient_id.age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', "Cancelled")], default='draft',
                             string="Status", tracking=True)
    reference = fields.Char(string='Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    note = fields.Text(string='Description')
    date_appointment = fields.Date(string="Date")
    date_checkup = fields.Datetime(string="Check Up Time")
    pharmacy_line_ids=fields.One2many('appointment.pharmacy','appointment_id', string="Medicine List")


    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, val):
        if not val.get('note'):
            val['note'] = 'New Patient'
        if val.get('name', _('New')) == _('New'):
            val['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        res = super(HospitalAppointment, self).create(val)
        return res

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
                if self.patient_id.note:
                    self.note = self.patient_id.note
                else:
                    self.gender = ''
                    self.note = ''


class AppointmentPharmacy(models.Model):
    _name="appointment.pharmacy"
    _description = "Appointment Pharmacy Lines"
    medicine_id=fields.Many2one('hospital.medicine')
    price_unit=fields.Float(related="medicine_id.price")
    qty_prod=fields.Integer(string="Quantity", default="1")
    appointment_id=fields.Many2one('hospital.appointment', string="medicine")


