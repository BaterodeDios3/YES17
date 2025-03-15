# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_presale = fields.Boolean(string='Print PreSale Receipt')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_presale = fields.Boolean(related='pos_config_id.enable_presale', readonly=False)
