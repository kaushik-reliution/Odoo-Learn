from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    """
    Task[2813]: Customer Credit Limit Management
    Working: active credit limit boolean field under invoice line check whether limit set or net.
    """
    _inherit = ['res.partner']

    active_credit_limit = fields.Boolean(string="Active Credit Limit", default=False, tracking=True)
    warning_amt = fields.Float(string="Warning Amount")
    blocking_amt = fields.Float(string="Blocking Amount")

    @api.constrains('warning_amt')
    def check_amount(self):
        if self.warning_amt >= self.blocking_amt:
            raise ValidationError("A Warning Amount should note be a greater than Blocking Amount")




















