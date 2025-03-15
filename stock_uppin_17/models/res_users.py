from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _check_user_groupseeee(self, user_id):
        """ Verifica si el usuario pertenece al grupo 'stock_uppin_17.group_gerencia_sale' """
        user = self.env['res.users'].search([('name', '=', user_id)], limit=1)
        group_name = 'stock_uppin_17.group_gerencia_sale'
        return any(group.name == group_name for group in user.groups_id)
