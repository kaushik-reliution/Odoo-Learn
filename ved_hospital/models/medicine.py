from odoo import api, fields, models, _


class MedicineDetails(models.Model):
    _name = "hospital.medicine"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Medicine Details"
    name = fields.Char('Name', index=True, required=True)
    price = fields.Float(string="Price", tracking=True, Required=True)
    qty=fields.Integer(string="Quantity", tracking=True, Required=True)










