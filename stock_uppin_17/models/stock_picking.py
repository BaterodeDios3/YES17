from odoo import fields, models, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sum_product_uom_qty = fields.Float(string='Sum Product Uom Qty', compute='_compute_sum_quantity', store=True)
    sum_quantity = fields.Float(string='Sum Quantity', compute='_compute_sum_quantity', store=True)

    @api.depends('move_ids_without_package.product_uom_qty', 'move_ids_without_package.quantity')
    def _compute_sum_quantity(self):
        for record in self:
            record.sum_product_uom_qty = sum(record.move_ids_without_package.mapped('product_uom_qty'))
            record.sum_quantity = sum(record.move_ids_without_package.mapped('quantity'))
