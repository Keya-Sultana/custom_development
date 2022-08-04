

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        super(SaleOrder, self).action_confirm()

        for order in self:
            # Send Group Notification
            partner_ids = []
            grp = self.env.ref('yuko_sales.group_sale_head')
            for u in grp.users:
                if u.partner_id:
                    partner_ids.append(u.partner_id.id)

            if partner_ids:
                order.message_post(body="This sales order is confirmed.",
                                partner_ids=partner_ids)