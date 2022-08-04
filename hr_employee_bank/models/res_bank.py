from odoo import models, fields


class ResBank(models.Model):
    _inherit = 'res.bank'

    bic = fields.Char('Bank Identifier Code', index=True, help="Sometimes called BIC or Swift.", required=True)

