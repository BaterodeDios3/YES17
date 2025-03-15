from odoo import models, fields, api
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # que no se duplique default_code
    @api.model
    def create(self, vals):
        if 'default_code' in vals:
            if self.env['product.template'].search_count([('default_code', '=', vals['default_code'])]) > 0:
                raise UserError('El codigo ya existe')
        return super(ProductTemplate, self).create(vals)

    def write(self, vals):
        if 'default_code' in vals:
            if self.env['product.template'].search_count([('default_code', '=', vals['default_code'])]) > 0:
                raise UserError('El codigo ya existe')
        return super(ProductTemplate, self).write(vals)
