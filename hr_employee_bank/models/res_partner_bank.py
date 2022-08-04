from odoo import models, fields

class BankAccount(models.Model):
    _inherit = 'res.partner.bank'

    bank_branch = fields.Char(string="Bank Branch")
    bank_account_title = fields.Char(string="Account Name")
    bank_nominee = fields.Char(string="Nominee Name")
    bank_nominee_nid = fields.Char(string="Nominee NID No")
    account_open_date = fields.Date(string="Account Opening Date")
    address = fields.Char(string="Nominee Address")
    mobile = fields.Char(string="Nominee Mobile No")
    swift_code = fields.Char('SWIFT Code', )



    
