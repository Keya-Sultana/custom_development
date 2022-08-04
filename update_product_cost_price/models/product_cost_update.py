from odoo import api, fields, models
from odoo.osv import osv
import datetime

class ProductCostUpdate(models.Model):
    _name = 'product.cost.update'
    _description = "Product Cost Update"
    
    name = fields.Char('Name', required=True)
    date= fields.Datetime('Date', default=datetime.date.today())
    line_ids = fields.One2many('product.cost.update.line', 'update_id', string='Product Lines')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ], string='Status', readonly=True, default='draft')
    
#     def _set_standard_price(self, product_id, cost_price):
#         prod_pool = self.env['product.product']
#         prod = prod_pool.search([('id', '=', product_id)])
#         prod.write({'standard_price': cost_price})
    
    @api.one
    def action_validate(self):
        for line in self.line_ids:
            line.product_id.write({'standard_price': line.new_cost_price})
            #self._set_standard_price(line.product_id.id, line.new_cost_price)
        self.write({'state': 'done'})
    
    @api.one
    def action_confirm(self):
        self.write({'state': 'confirm'})
        
    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state not in ['draft']:
                raise osv.except_osv(('Warning!'), ('You cannot delete the record! It is in %s state.') % (rec.state))
        return super(ProductCostUpdate, self).unlink()
    

class ProductCostUpdateLine(models.Model):
    _name = 'product.cost.update.line'
    update_id = fields.Many2one('product.cost.update', string='Update', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    old_cost_price = fields.Float('Old Cost Price')
    new_cost_price = fields.Float('New Cost Price')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ], string='Status', readonly=True, default='draft')
    
#     @api.one
#     @api.onchange('product_id')
#     def onchange_product_id(self):
#         self.old_cost_price = self.product_id.standard_price
    