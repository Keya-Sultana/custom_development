from odoo import api, fields, models, _


class StockMoveReport(models.AbstractModel):
    _name = 'report.yuko_inventory_reports.report_stock_move_qweb'

    def generate_report_data(self, data):
        date_start = data['date_from']
        date_to = data['date_to']
        # product_id = data['product_id']

        sql = '''SELECT sm.product_id
                    FROM stock_move sm
                LEFT JOIN product_product pp 
                   ON sm.product_id = pp.id 
                LEFT JOIN product_template pt 
                   ON pp.product_tmpl_id = pt.id
                WHERE Date(sm.date) BETWEEN '%s' AND '%s' ''' % (date_start, date_to)

        self.env.cr.execute(sql)

        return {'lists': self.env.cr.execute(sql)}

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        lists = self.generate_report_data(data)
        docargs = {
            'doc_ids': self._ids,
            'docs': self,
            'record': data,
            'lines': lists['lists'],
        }
        return report_obj.render('yuko_inventory_reports.report_stock_move_qweb', docargs)


