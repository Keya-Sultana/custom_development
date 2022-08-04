from odoo import api, fields, tools, models, _
from odoo.exceptions import UserError


class BusinessCategoryType(models.Model):
    _name = 'business.category.type'
    _description = 'Business Category Type'

    name = fields.Char('Name', required=True, translate=True)