from odoo import api, fields, tools, models, _
from odoo.exceptions import UserError


class ShippingMethodType(models.Model):
    _name = 'shipping.method.type'
    _description = 'Shipping Method Type'

    name = fields.Char('Name', required=True, translate=True)