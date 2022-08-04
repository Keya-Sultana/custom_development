from odoo import api, fields, tools, models, _
from odoo.exceptions import UserError


class AssetCategoryType(models.Model):
    _name = 'asset.category.type'
    _description = 'Asset Category Type'

    name = fields.Char('Name', required=True, translate=True)