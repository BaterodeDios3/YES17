# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _



class OrderLineInherit(models.Model):
    _inherit = "sale.order.line"

    chk_user_grp = fields.Boolean(string="Check User",compute="_onchange_user_group")

    @api.depends('product_id')
    def _onchange_user_group(self):
        if self.user_has_groups('sales_team.group_sale_manager'):
            self.chk_user_grp = True
        else:
            self.chk_user_grp = False

