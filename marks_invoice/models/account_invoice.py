from odoo import api, fields, models, _

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    @api.multi
    def amount_to_text(self, amount_total):
        amt_to_word = self.env['res.currency'].amount_to_word(amount_total)
        return amt_to_word
    
    @api.one
    @api.depends('invoice_line_ids.total_discount', 'invoice_line_ids.amount_total', 'tax_line_ids.amount')
    def _compute_amount_discount(self):
        self.amount_discount = sum(line.total_discount for line in self.invoice_line_ids)
        self.amount_undiscount = sum(line.amount_total for line in self.invoice_line_ids)
        self.amount_tax = sum(line.amount for line in self.tax_line_ids)
        self.sub_amount = self.amount_undiscount - self.amount_discount
        self.total_amount = self.sub_amount + self.amount_tax

    amount_discount = fields.Monetary(string='Discount Amount',
        store=True, readonly=True, compute='_compute_amount_discount', track_visibility='always')
    amount_undiscount = fields.Monetary(string='Undiscount Amount',
        store=True, readonly=True, compute='_compute_amount_discount', track_visibility='always')
    sub_amount = fields.Monetary(string='Subtotal Amount',
        store=True, readonly=True, compute='_compute_amount_discount')
    total_amount = fields.Monetary(string='Total Amount',
        store=True, readonly=True, compute='_compute_amount_discount')
    
    
class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'  
    
    @api.one
    @api.depends('price_unit', 'discount', 'quantity')
    def _comput_total_discount(self):
        self.total_discount = (self.quantity * self.price_unit) * ((self.discount or 0.0) / 100.0)
        print"======self.total_discount====="
    
    
    @api.one
    @api.depends('price_unit', 'quantity')
    def _comput_total_amount(self):
        self.amount_total = self.quantity * self.price_unit
    
    
    
    total_discount = fields.Monetary(string='Total Discount',
        store=True, readonly=True, compute='_comput_total_discount')   
    
    amount_total = fields.Monetary(string='Total amount',
        store=True, readonly=True, compute='_comput_total_amount')      