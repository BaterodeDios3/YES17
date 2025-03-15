from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_presale = fields.Boolean(related='pos_config_id.enable_presale', readonly=False)
