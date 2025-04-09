from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    cannot_edit_pricelist = fields.Boolean(
        string="No puede editar precios",
        compute="_compute_cannot_edit_pricelist",
        readonly="True",
    )

    @api.depends("partner_id")
    def _compute_cannot_edit_pricelist(self):
        for record in self:
            record.cannot_edit_pricelist = self.env.user.has_group(
                "yestore_price_in_sale.group_edit_pricelist"
            )


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    cannot_edit_pricelist = fields.Boolean(
        related="order_id.cannot_edit_pricelist", readonly="True"
    )
