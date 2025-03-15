# Copyright 2020, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class StockKardexReport(models.Model):
    _name = 'stock.kardex.report'
    _description = 'This model creates a kardex report for stock moves'
    _order = 'date desc'



    move_id = fields.Many2one('stock.move', readonly=True, string='Movimiento')
    product_id = fields.Many2one('product.product', readonly=True, string='Producto')
    product_uom_id = fields.Many2one('uom.uom', readonly=True, string='Unidad de Medida')
    # lot_id = fields.Many2one('stock.production.lot', readonly=True)
    owner_id = fields.Many2one('res.partner', readonly=True, string='Propietario')
    package_id = fields.Many2one('stock.quant.package', readonly=True, string='Paquete')
    location_id = fields.Many2one('stock.location', readonly=True, string='Origen')
    location_dest_id = fields.Many2one('stock.location', readonly=True, string='Destino')
    qty_done = fields.Float('Cantidad', readonly=True)
    qty_in = fields.Float('Entrada', readonly=True)
    qty_out = fields.Float('Salida', readonly=True)
    date = fields.Datetime(readonly=True, string='Fecha')
    origin = fields.Char(readonly=True, string='Movimiento', related='move_id.origin')
    reference = fields.Char(readonly=True, string='Referencia')
    balance = fields.Float(readonly=True, string='Saldo')
    user_id = fields.Many2one('res.users', readonly=True, string='Usuario')
    update_at = fields.Datetime(readonly=True, string='Fecha Modificacion')
    picking_type_id = fields.Many2one('stock.picking.type', readonly=True, string='Tipo de Movimiento')
    tipo_mov = fields.Char(readonly=True, string='Tipo Movimiento')
    cost = fields.Float('Costo', readonly=True)
    total_cost = fields.Float('Costo Total', readonly=True)


    def action_open_reference(self):
        """ Open the form view of the move's reference document, if one exists, otherwise open form view of self
        """
        self.ensure_one()
        source = self.move_id
        if source and source.check_access_rights('read', raise_exception=False):
            return {
                'res_model': source._name,
                'type': 'ir.actions.act_window',
                'views': [[False, "form"]],
                'res_id': source.id,
            }
        return {
            'res_model': self._name,
            'type': 'ir.actions.act_window',
            'views': [[False, "form"]],
            'res_id': self.id,
        }