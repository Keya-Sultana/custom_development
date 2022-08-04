from odoo import api, fields, tools, models, _
from odoo.exceptions import UserError


class ShippingPortType(models.Model):
    _name = 'shipping.port.type'
    _description = 'Shipping Port Type'

    name = fields.Char('Name', required=True, translate=True)