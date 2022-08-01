from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    """
    Task[2813]: Customer Credit Limit Management
    Working: active credit limit boolean field under invoice line check whether limit set or net.
    """
    _inherit = 'res.partner'

    credit_limit = fields.Boolean(string="Credit Limit", default=False)
    credit_limit_amount = fields.Float(string="Credit Limit", default=0.0, tracking=True)

    @api.constrains('credit_limit_amount')
    def check_amount(self):
        if self.credit_limit:
            if self.credit_limit_amount <= 0.0:
                raise ValidationError("Credit Limit should be greater than zero!")
