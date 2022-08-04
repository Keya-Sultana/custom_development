from odoo import api, fields, tools, models, _
from odoo.exceptions import UserError


class PaymentType(models.Model):
    _name = 'payment.type'
    _description = 'Payment Method Type'

    name = fields.Char('Name', required=True, translate=True)