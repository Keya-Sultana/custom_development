from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import time

AVAILABLE_PRIORITIES = [
    ('0', 'Normal'),
    ('1', 'Good'),
    ('2', 'Very Good'),
    ('3', 'Excellent')
]


class ResPartner(models.Model):
    _inherit = "res.partner"
    _order = "priority desc"


    # bin_no = fields.Char('BIN No', )
    # tin_no = fields.Char('TIN No', )
    credit_limit = fields.Char('Credit Limit', )
    entry_date = fields.Date('Customer Entry Date', readonly=True, default=fields.Datetime.now)
    alt_mobile = fields.Char('Alt. Mobile No', )
    alt_email = fields.Char('Alt. Email', )
    alt_phone = fields.Char('Alt. Phone No', )
    reg_no = fields.Char('Company Reg. No', )
    founded_date = fields.Date('Founded on Date', )
    #bank_ac = fields.Char('Bank A/C', )
    #bank_name = fields.Char('Bank Name', )
    #branch_name = fields.Char('Branch Name', )
    #swift_code = fields.Char('Branch Name', )
    billing_address = fields.Char('Billing Address', )
    shipping_addresss = fields.Char('Shipping Address', )
    priority = fields.Selection(AVAILABLE_PRIORITIES, "Customer Rating", default='0')

    business_type = fields.Many2one('business.category.type', string="Business Category")
    zip_id = fields.Char('Zip')


