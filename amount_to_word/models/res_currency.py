from odoo import api, fields, models
from odoo.tools import amount_to_text_en

class ResCurrency(models.Model):
    _inherit = 'res.currency'
    #Do not touch _name it must be same as _inherit
       
    unit_string = fields.Char('Unit Translation', size=10)
    decimal_string = fields.Char('Decimal Translation', size=10)
       
    def amount_to_text(self, amount, lang='en'):        
        a = self.unit_string if self.unit_string else ""
        b = self.decimal_string if self.decimal_string else ""
        convert_amount_in_words = amount_to_text_en.amount_to_text(amount, lang, a)
        print convert_amount_in_words
        return convert_amount_in_words.replace('Cents', b).replace('Cent', b)