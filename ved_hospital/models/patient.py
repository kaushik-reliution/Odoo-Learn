from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalManagement(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _description = "Patient  Detail"
    name = fields.Char(string='Name', required=True, tracking=True)
    reference = fields.Char(string='Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string="Description")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', "Cancelled")], default='draft',
                             string="Status", tracking=True)
    responsible_id = fields.Many2one('res.partner', string="Responsible")
    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Name must be unique'),
        ('unique_age', 'check(age > 0)', 'Age cannot be zero')
    ]
    appoint_cnt = fields.Integer(string="Appointment Count", compute='_compute_appoint_cnt')
    active = fields.Boolean("Active", default=True)
    m_ids = fields.Many2many('hospital.medicine', string="Medicines")

    def _compute_appoint_cnt(self):
        for rec in self:
            appoint_cnt = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            # Working of compute method:---> select count(*) from  hospital.appoint where patient_id=39
            rec.appoint_cnt = appoint_cnt

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
        if val.get('reference', _('New')) == _('New'):
            val['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        res = super(HospitalManagement, self).create(val)
        return res

    def name_get(self):
        # patient_list = []
        # for record in self:
        #     name = record.reference + record.name
        #     patient_list.append((record.id, name))
        return[(record.id, "%s  : %s" %(record.reference,record.name))for record in self]

    # @api.constrains('name')
    # def check_name(self):
    #     for rec in self:
    #         patients = self.env['hospital.patient'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
    #         if patients:
    #             raise ValidationError(_("Name %s is already exits" % rec.name))
    #
    # @api.constrains('age')
    # def check_age(self):
    #     for rec in self:
    #         if rec.age == 0:
    #             raise ValidationError(_("Age cannot be Zero....!"))
