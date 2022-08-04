from odoo import api, exceptions, fields, models
from odoo.tools.misc import formatLang


class MrrReport(models.AbstractModel):
    _inherit = 'report.stock_picking_mrr.report_mrr_doc'



    def get_rep_line(self,report_utility_pool,picking,new_picking,po_ids):
        pack_list = []
        total_amount = []
        po_no = []
        po_date = ''
        if po_ids:
            for po in po_ids:
                po_no.append(po.name)
                po_date = report_utility_pool.getERPDateFormat(report_utility_pool.getDateTimeFromStr(po.date_order))
                customer = po.partner_id.name
                challan = picking.challan_bill_no
                challan_date = report_utility_pool.getERPDateFormat(report_utility_pool.getDateTimeFromStr(picking.date_done))
                for move in new_picking.pack_operation_ids:
                    po_line_objs = po.order_line.filtered(lambda r: r.product_id.id == move.product_id.id)
                    if po_line_objs:
                        pack_obj = {}
                        # calculate discount amount
                        dis_amt = po_line_objs[0].price_unit / 100
                        pack_obj['product_id'] = move.product_id.display_name
                        pack_obj['pr_no'] = po.origin
                        pack_obj['mrr_quantity'] = move.qty_done
                        pack_obj['product_qty'] = po_line_objs[0].product_qty
                        pack_obj['product_uom_id'] = move.product_uom_id.name
                        pack_obj['price_unit'] = formatLang(self.env, po_line_objs[0].price_unit)
                        #pack_obj['sub_amount'] = formatLang(self.env, move.qty_done * (po_line_objs[0].price_unit - dis_amt))
                        pack_obj['sub_amount'] = formatLang(self.env, move.qty_done * po_line_objs[0].price_unit)
                        pack_obj['discount'] = False
                        #pack_obj['amount'] = move.qty_done * (po_line_objs[0].price_unit - dis_amt)
                        pack_obj['amount'] = move.qty_done * po_line_objs[0].price_unit
                        total_amount.append(pack_obj['amount'])
                        pack_list.append(pack_obj)
        else:
            customer = picking.partner_id.name
            challan = picking.challan_bill_no
            challan_date = report_utility_pool.getERPDateFormat(
                report_utility_pool.getDateTimeFromStr(picking.date_done))
            for move in new_picking.pack_operation_ids:
                pack_obj = {}
                pack_obj['product_id'] = move.product_id.display_name
                pack_obj['pr_no'] = new_picking.origin
                pack_obj['product_qty'] = False
                pack_obj['mrr_quantity'] = move.qty_done
                pack_obj['product_uom_id'] = move.product_uom_id.name
                pack_obj['price_unit'] = formatLang(self.env, move.product_id.standard_price)
                pack_obj['sub_amount'] = formatLang(self.env, move.qty_done * move.product_id.standard_price)
                pack_obj['discount'] = False
                pack_obj['amount'] = move.qty_done * move.product_id.standard_price
                total_amount.append(pack_obj['amount'])
                pack_list.append(pack_obj)

        return {
            'pack_list':pack_list,
            'po_no':po_no,
            'po_date':po_date,
            'customer':customer,
            'challan':challan,
            'challan_date':challan_date,
            'total_amount': total_amount
        }