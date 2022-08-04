# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = "stock.move"

    product_cat_id = fields.Many2one('product.category', 'Product Category',related='product_id.categ_id', store=True)