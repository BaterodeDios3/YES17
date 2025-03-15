from odoo import models, fields, api

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _check_user_groups(self, user):
        """
        Método para verificar si un usuario pertenece a un grupo específico
        :param user: El objeto del usuario para verificar sus grupos
        :return: True si el usuario pertenece al grupo, False si no
        """
        thUser = self.env['res.users'].search([('name', '=', user.name)], limit=1)
        group_name = 'stock_uppin_17.group_gerencia_sale'
        if any(group.name == group_name for group in thUser.groups_id):
            return True
        return False

    def _loader_params_hr_employee(self):
        result = super()._loader_params_hr_employee()

        # Obtener el usuario actual
        user = self.env.user  # Usuario actual de la sesión

        # Verificar los grupos del usuario
        if self._check_user_groups(user):
            # Si pertenece al grupo, puedes agregar permisos adicionales
            result['search_params']['fields'].extend(
                ['disable_cost', 'disable_payment', 'disable_customer']
            )
        return result