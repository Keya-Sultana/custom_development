
from odoo import api, exceptions, fields, models
import time



class StockMoveWizard(models.TransientModel):
    _name = 'stock.move.wizard'


    product_id = fields.Many2one('product.template', string='Product',)
    from_date = fields.Date('Date From', required=True)
    to_date = fields.Date('Date To', required=True)
    stock_location_id = fields.Many2one('stock.location', string='Location')



    @api.multi
    def process_report(self):
        data = {
            'date_from': self.from_date,
            'date_to': self.to_date,
            'product_id': self.product_id.id,
            'product_name': self.product_id.name,
        }

        return self.env['report'].get_action(self, 'yuko_inventory_reports.report_stock_move_qweb',
                                             data=data)

