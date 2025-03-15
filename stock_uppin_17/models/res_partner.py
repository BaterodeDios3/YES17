from odoo import fields, models, api
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Agregar restriccion donde el campo phone o el campo mobile sean unicos para metodo crear y escribir

    @api.model
    def create(self, vals):
        if 'phone' in vals:
            if self.env['res.partner'].search_count([('phone', '=', vals['phone']), ('phone', '!=', 0), ('phone', '!=', False)]) > 0:
                raise UserError('El telefono ya existe')
        if 'mobile' in vals:
            if self.env['res.partner'].search_count([('mobile', '=', vals['mobile']), ('mobile', '!=', 0), ('mobile', '!=', False)]) > 0:
                raise UserError('El celular ya existe')
        return super(ResPartner, self).create(vals)

    def write(self, vals):
        if 'phone' in vals:
            if self.env['res.partner'].search_count([('phone', '=', vals['phone']), ('phone', '!=', 0), ('phone', '!=', False)]) > 0:
                raise UserError('El telefono ya existe')
        if 'mobile' in vals:
            if self.env['res.partner'].search_count([('mobile', '=', vals['mobile']), ('mobile', '!=', 0), ('mobile', '!=', False)]) > 0:
                raise UserError('El celular ya existe')
        return super(ResPartner, self).write(vals)

