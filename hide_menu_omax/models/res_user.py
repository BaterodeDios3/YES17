# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from collections import defaultdict
from odoo.exceptions import MissingError, AccessError
from odoo.tools import frozendict


class ResUsers(models.Model):
    _inherit = 'res.users'

    menu_ids = fields.Many2many('ir.ui.menu', 'user_menu_rel', 'user_id', 'menu_id', string='Menu To Hide', help='Select Menus To Hide From This User')
    report_ids = fields.Many2many('ir.actions.report', 'user_report_rel', 'user_id', 'report_id', 'Hide Report',
                                  help='Select Report To Hide From This User')

    @api.model
    def create(self, values):
        self.env['ir.ui.menu'].clear_caches()
        return super(ResUsers, self).create(values)

    def write(self, values):
        self.env['ir.ui.menu'].clear_caches()
        return super(ResUsers, self).write(values)


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def create(self, values):
        self.env['ir.ui.menu'].clear_caches()
        return super(IrUiMenu, self).create(values)

    def write(self, values):
        self.env['ir.ui.menu'].clear_caches()
        return super(IrUiMenu, self).write(values)

    @api.model
    @tools.ormcache('frozenset(self.env.user.groups_id.ids)', 'debug')
    def _visible_menu_ids(self, debug=False):
        menus = super(IrUiMenu, self)._visible_menu_ids(debug)
        if self._uid != SUPERUSER_ID:
            user = self.env['res.users'].browse(self._uid)
            for menu in user.menu_ids:
                menus.discard(menu.id)
        return menus

class IrActions(models.Model):
    _inherit = 'ir.actions.actions'

    @tools.ormcache('model_name', 'self.env.lang')
    def _get_bindings(self, model_name):
        cr = self.env.cr

        # discard unauthorized actions, and read action definitions
        result = defaultdict(list)

        self.env.flush_all()
        cr.execute("""
            SELECT a.id, a.type, a.binding_type
              FROM ir_actions a
              JOIN ir_model m ON a.binding_model_id = m.id
             WHERE m.model = %s
          ORDER BY a.id
        """, [model_name])
        for action_id, action_model, binding_type in cr.fetchall():
            try:
                if self.env.user.id != SUPERUSER_ID and action_id in self.env.user.report_ids.ids and action_model == 'ir.actions.report':
                    pass
                else:
                    action = self.env[action_model].sudo().browse(action_id)
                    fields = ['name', 'binding_view_types']
                    for field in ('groups_id', 'res_model', 'sequence'):
                        if field in action._fields:
                            fields.append(field)
                    action = action.read(fields)[0]
                    if action.get('groups_id'):
                        groups = self.env['res.groups'].browse(action['groups_id'])
                        action['groups_id'] = ','.join(ext_id for ext_id in groups._ensure_xml_id().values())
                    result[binding_type].append(frozendict(action))
            except (MissingError):
                continue
        # sort actions by their sequence if sequence available
        if result.get('action'):
            result['action'] = tuple(sorted(result['action'], key=lambda vals: vals.get('sequence', 0)))
        return frozendict(result)

