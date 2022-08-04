from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.translate import _


class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'


    sub_category_id = fields.Many2one('asset.category.type', string='Sub Category', required=True, change_default=True, readonly=True, states={'draft': [('readonly', False)]})




