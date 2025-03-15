# Copyright 2020, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from datetime import datetime, time, timedelta

from odoo import _, fields, models
import textwrap


class StockKardexReportWiz(models.TransientModel):
    _name = 'stock.kardex.report.wiz'
    _description = 'Wizard to create kardex report of stock moves'

    date_from = fields.Datetime(string='Desde', required=True, default=lambda self: datetime.combine(fields.Datetime.now().date(), time.min))
    date_to = fields.Datetime(string='Hasta', required=True, default=lambda self: datetime.combine(fields.Datetime.now().date(), time.max ))
    product = fields.Many2one('product.product', required=True, string='Producto')
    location = fields.Many2one('stock.location', required=True, string='Ubicación')

    def open_table(self):
        product_id = self.product
        location_id = self.location
        date_from = self.date_from
        date_to = self.date_to
        company_id = self.env.company  # Obtén la compañía actual directamente

        self.env['stock.kardex.report'].search([]).unlink()
        total = 0

        if location_id.id:
            # Obtener movimientos y costos
            self._cr.execute("""
            WITH one AS (
                SELECT
                    sml.product_id, 
                    sml.product_uom_id,
                    sml.owner_id, 
                    sml.package_id,
                    sml.quantity, 
                    sml.move_id, 
                    sml.location_id,
                    sml.location_dest_id, 
                    sm.date, 
                    sm.origin,
                    sml.reference,
                    sml.state,
                    sml.write_uid,
                    sml.write_date,
                    sm.picking_type_id
                FROM stock_move_line sml
                INNER JOIN stock_move sm ON sml.move_id = sm.id
                WHERE 
                    sm.date >= %s
                    and sm.date <= %s
                    AND sm.company_id = %s
            ),
            two AS (
                SELECT *
                FROM one
                WHERE location_id = %s OR location_dest_id = %s
            )
            SELECT two.*, svl.unit_cost, (two.quantity * svl.unit_cost) AS total_cost
            FROM two
            LEFT JOIN stock_valuation_layer svl ON svl.stock_move_id = two.move_id
            WHERE two.product_id = %s AND two.state = 'done'
            ORDER BY two.date;
            """, [
                date_from, date_to, company_id.id,
                location_id.id, location_id.id,
                product_id.id
            ])
        else:
            # Obtener movimientos y costos sin ubicación específica
            self._cr.execute("""
            WITH one AS (
                SELECT
                    sml.product_id, 
                    sml.product_uom_id,
                    sml.owner_id, 
                    sml.package_id,
                    sml.quantity, 
                    sml.move_id, 
                    sml.location_id,
                    sml.location_dest_id, 
                    sm.date, 
                    sm.origin,
                    sml.reference,
                    sml.state,
                    sml.write_uid,
                    sml.write_date,
                    sm.picking_type_id
                FROM stock_move_line sml
                INNER JOIN stock_move sm ON sml.move_id = sm.id
                WHERE sm.date >= %s and sm.date <= %s AND sm.company_id = %s
            )
            SELECT one.*, svl.unit_cost, (one.quantity * svl.unit_cost) AS total_cost
            FROM one
            LEFT JOIN stock_valuation_layer svl ON svl.stock_move_id = one.move_id
            WHERE one.product_id = %s AND one.state = 'done'
            ORDER BY one.date;
            """, [
                date_from, date_to, company_id.id,
                product_id.id
            ])

        moves = self._cr.dictfetchall()
        report_list = []
        seen_moves = set()

        for rec in moves:
            move_id = rec['move_id']
            if move_id in seen_moves:
                continue
            seen_moves.add(move_id)

            done_qty = rec['quantity']
            qty_in = 0
            qty_out = 0

            if location_id.id:
                if rec['location_id'] == location_id.id:
                    qty_out = done_qty  # Salida
                else:
                    qty_in = done_qty  # Entrada
                total += (qty_in - qty_out)
            else:
                if self.env['stock.location'].browse(rec['location_id']).usage in ['internal', 'transit'] and self.env[
                    'stock.location'].browse(rec['location_dest_id']).usage not in ['internal', 'transit']:
                    qty_out = done_qty  # Salida
                else:
                    qty_in = done_qty  # Entrada
                total += (qty_in - qty_out)

            origin = textwrap.shorten(rec['origin'], width=80, placeholder="...") if rec['origin'] else ''

            cost = rec['unit_cost'] if rec['unit_cost'] else 0
            total_cost = rec['total_cost'] if rec['total_cost'] else 0
            thTipoMov = ''
            xTipoMov = self.env['stock.picking.type'].browse(rec['picking_type_id']).code
            if xTipoMov == 'incoming':
                thTipoMov = 'Recepción'
            elif xTipoMov == 'outgoing':
                thTipoMov = 'Entrega'
            elif xTipoMov == 'mrp_operation':
                thTipoMov = 'Fabricación'
            elif xTipoMov == 'internal':
                thTipoMov = 'Transferencia Interna'
            else:
                thTipoMov = 'Indefinido'

            line = {
                'move_id': rec['move_id'],
                'product_id': rec['product_id'],
                'product_uom_id': rec['product_uom_id'],
                'owner_id': rec['owner_id'],
                'package_id': rec['package_id'],
                'qty_in': qty_in,
                'qty_out': qty_out,
                'location_id': rec['location_id'],
                'location_dest_id': rec['location_dest_id'],
                'tipo_mov': thTipoMov,
                'date': rec['date'],
                'balance': total,
                'origin': origin,
                'reference': rec['reference'],
                'user_id': rec['write_uid'],
                'update_at': rec['write_date'],
                'picking_type_id': rec['picking_type_id'],
                'cost': cost,
                'total_cost': total_cost,
            }
            report_list.append(line)

        self.env['stock.kardex.report'].create(report_list)

        tree_view_id = self.env.ref('stock_kardex_report.stock_kardex_report_tree_view').id
        action = {
            'type': 'ir.actions.act_window',
            'views': [(tree_view_id, 'tree')],
            'view_id': tree_view_id,
            'view_mode': 'tree',
            'name': _('Stock Report'),
            'res_model': 'stock.kardex.report',
        }
        return action

