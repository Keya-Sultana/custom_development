from odoo import api, fields, models, _
from openerp.osv import osv
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    port_type = fields.Many2one('shipping.port.type',
                                   string="Shipping Port")
    payment_type = fields.Many2one('payment.type',
                                   string="Payment Method")
    method_type = fields.Many2one('shipping.method.type',
                                   string="Shipping Method")
    template_type = fields.Many2one('template.type',
                                string="Template")
    ter_condition = fields.Text("Terms & Conditions ")

    delivery_term = fields.Char('Shipping/Delivery terms')
    create_uid = fields.Many2one('res.users','Author',readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Purchaser Name', required=True)

    terms_type = fields.Selection([
        ('local', 'Local'),
        ('foreign', 'Foreign'),
    ], string='Terms Type', default='local')

    partner_attention_id = fields.Many2one('res.partner', string='Vendor Attention',
                                          states=READONLY_STATES,
                                          change_default=True, track_visibility='always')

    @api.onchange('template_type')
    def _onchange_template(self):
        if self.template_type:
            self.ter_condition = self.template_type.template

    @api.multi
    def button_confirm(self):
        for order in self:
            for line in order.order_line:
                if line.price_unit <= 0:
                    raise osv.except_osv(_('Warning!'), _('You cannot confirm without Unit Price.'))
        return super(PurchaseOrder, self).button_confirm()

    # @api.onchange('requisition_id')
    # def _onchange_requisition_id(self):
    #     if not self.requisition_id:
    #         return
    #
    #     requisition = self.requisition_id
    #     if self.partner_id:
    #         partner = self.partner_id
    #     else:
    #         partner = requisition.vendor_id
    #     payment_term = partner.property_supplier_payment_term_id
    #     currency = partner.property_purchase_currency_id or requisition.company_id.currency_id
    #
    #     FiscalPosition = self.env['account.fiscal.position']
    #     fpos = FiscalPosition.get_fiscal_position(partner.id)
    #     fpos = FiscalPosition.browse(fpos)
    #
    #     self.partner_id = partner.id
    #     self.fiscal_position_id = fpos.id
    #     self.payment_term_id = payment_term.id
    #     self.company_id = requisition.company_id.id
    #     self.currency_id = currency.id
    #     self.origin = requisition.name
    #     #self.partner_ref = requisition.name  # to control vendor bill based on agreement reference
    #     self.notes = requisition.description
    #     self.date_order = requisition.date_end or fields.Datetime.now()
    #     self.picking_type_id = requisition.picking_type_id.id
    #
    #     if requisition.type_id.line_copy != 'copy':
    #         return
    #
    #     # Create PO lines if necessary
    #     order_lines = []
    #     for line in requisition.line_ids:
    #         # Compute name
    #         product_lang = line.product_id.with_context({
    #             'lang': partner.lang,
    #             'partner_id': partner.id,
    #         })
    #         name = product_lang.display_name
    #         if product_lang.description_purchase:
    #             name += '\n' + product_lang.description_purchase
    #
    #         # Compute taxes
    #         if fpos:
    #             taxes_ids = fpos.map_tax(line.product_id.supplier_taxes_id.filtered(
    #                 lambda tax: tax.company_id == requisition.company_id)).ids
    #         else:
    #             taxes_ids = line.product_id.supplier_taxes_id.filtered(
    #                 lambda tax: tax.company_id == requisition.company_id).ids
    #
    #         # Compute quantity and price_unit
    #         if line.product_uom_id != line.product_id.uom_po_id:
    #             product_qty = line.product_uom_id._compute_quantity(line.product_ordered_qty, line.product_id.uom_po_id)
    #             price_unit = line.product_uom_id._compute_price(line.price_unit, line.product_id.uom_po_id)
    #         else:
    #             product_qty = line.product_ordered_qty
    #             price_unit = line.price_unit
    #
    #         if requisition.type_id.quantity_copy != 'copy':
    #             product_qty = 0
    #
    #         # Compute price_unit in appropriate currency
    #         if requisition.company_id.currency_id != currency:
    #             price_unit = requisition.company_id.currency_id.compute(price_unit, currency)
    #
    #         # Create PO line
    #         order_lines.append((0, 0, {
    #             'name': name,
    #             'product_id': line.product_id.id,
    #             'product_uom': line.product_id.uom_po_id.id,
    #             'product_qty': product_qty,
    #             'price_unit': price_unit,
    #             'taxes_id': [(6, 0, taxes_ids)],
    #             'date_planned': requisition.schedule_date or fields.Date.today(),
    #             'procurement_ids': [(6, 0, [requisition.procurement_id.id])] if requisition.procurement_id else False,
    #             'account_analytic_id': line.account_analytic_id.id,
    #         }))
    #     self.order_line = order_lines
