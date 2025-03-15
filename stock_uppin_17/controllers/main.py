from odoo import http
import json


class StockUppinController(http.Controller):

    @http.route('/stock_uppin_17/get_user_groups', auth='user', type='http')
    def get_user_groups(self):
        # Obtener los grupos del usuario actual
        user_groups = http.request.env.user.groups_id.mapped('name')

        # Crear un diccionario con el resultado que deseas devolver
        response_data = {
            'groups': user_groups
        }

        # Devuelve los grupos en formato JSON
        return http.Response(
            json.dumps(response_data),
            content_type='application/json; charset=utf-8',
            status=200
        )
