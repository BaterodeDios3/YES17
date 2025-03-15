# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
#################################################################################
from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    pos_config = fields.Many2one(
        'pos.config', string='Default Point of Sale', domain=[('active', '=', True)])

    @api.onchange('pos_config')
    def onchange_pos_config(self):
        self.env.registry.clear_cache()

    def write(self, vals):
        self.env.registry.clear_cache()
        return super(ResUsers, self).write(vals)
