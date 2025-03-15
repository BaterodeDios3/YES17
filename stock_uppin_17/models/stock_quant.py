import math

from odoo import fields, models, api, tools, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_pacbulto = fields.Char(string='pacbulto', store=True)
    x_pcpackage = fields.Char(string='pcpackage', store=True)
    x_pcsbulto = fields.Char(string='pcsbulto', store=True)

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    pck_bulto = fields.Float(string='Pac/Bulto', readonly=True, store=True, compute='_compute_pcs')
    pc_package = fields.Float(string='Pac/Package', readonly=True, store=True, compute='_compute_pcs')
    pc_bulto = fields.Float(string='Pc/Bulto', readonly=True, store=True, compute='_compute_pcs')

    
    @api.depends('product_id', 'inventory_quantity_auto_apply')
    def _compute_pcs(self):
        for record in self:
            if record.inventory_quantity_auto_apply:

                if record.product_id.x_pcsbulto and record.product_id.x_pcsbulto.isnumeric() and float(record.product_id.x_pcsbulto) != 0 and record.inventory_quantity_auto_apply != 0 :
                    record.pc_bulto = math.floor(record.inventory_quantity_auto_apply / float(record.product_id.x_pcsbulto))
                else:
                    record.pc_bulto = 0

                if record.product_id.x_pcpackage and record.product_id.x_pcpackage.isnumeric() and float(record.product_id.x_pcpackage) != 0 and record.inventory_quantity_auto_apply != 0:
                    record.pc_package = math.floor(record.inventory_quantity_auto_apply / float(record.product_id.x_pcpackage))
                else:
                    record.pc_package = 0

                if record.product_id.x_pacbulto and record.product_id.x_pacbulto.isnumeric() and float(record.product_id.x_pacbulto) != 0 and record.inventory_quantity_auto_apply != 0:
                    record.pck_bulto = math.floor(record.inventory_quantity_auto_apply / float(record.product_id.x_pacbulto))
                else:
                    record.pck_bulto = 0 

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    pck_bulto = fields.Float(string='Pac/Bulto', readonly=True, store=True, compute='_compute_pcs')
    pc_package = fields.Float(string='Pac/Package', readonly=True, store=True, compute='_compute_pcs')
    pc_bulto = fields.Float(string='Pc/Bulto', readonly=True, store=True, compute='_compute_pcs')
    x_price_total = fields.Monetary(string='Precio Total', readonly=True, compute='_compute_total')

    @api.depends('price_unit', 'quantity')
    def _compute_total(self):
        for record in self:
            record.x_price_total = record.price_unit * record.quantity

    @api.depends('product_id', 'quantity')
    def _compute_pcs(self):
        for record in self:
            if record.quantity:
                if record.product_id.x_pcsbulto and record.product_id.x_pcsbulto.isnumeric() and float(record.product_id.x_pcsbulto) != 0 and record.quantity != 0:
                    record.pc_bulto = math.floor(record.quantity / float(record.product_id.x_pcsbulto))
                else:
                    record.pc_bulto = 0

                if record.product_id.x_pcpackage and record.product_id.x_pcpackage.isnumeric() and float(record.product_id.x_pcpackage) != 0 and record.quantity != 0:
                    record.pc_package = math.floor(record.quantity / float(record.product_id.x_pcpackage))
                else:
                    record.pc_package = 0

                if record.product_id.x_pacbulto and record.product_id.x_pacbulto.isnumeric() and float(record.product_id.x_pacbulto) != 0 and record.quantity != 0:
                    record.pck_bulto = math.floor(record.pc_package / float(record.product_id.x_pacbulto))
                else:
                    record.pck_bulto = 0

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    pck_bulto = fields.Float(string='Pac/Bulto', readonly=True, store=True, compute='_compute_pcs')
    pc_package = fields.Float(string='Pac/Package', readonly=True, store=True, compute='_compute_pcs')
    pc_bulto = fields.Float(string='Pc/Bulto', readonly=True, store=True, compute='_compute_pcs')
    x_price_total = fields.Monetary(string='Precio Total', readonly=True, compute='_compute_total')

    @api.depends('price_unit', 'product_uom_qty')
    def _compute_total(self):
        for record in self:
            record.x_price_total = record.price_unit * record.product_uom_qty

    @api.depends('product_id', 'product_uom_qty')
    def _compute_pcs(self):
        for record in self:
            if record.product_uom_qty:
                if record.product_id.x_pcsbulto and record.product_id.x_pcsbulto.isnumeric() and float(record.product_id.x_pcsbulto) != 0 and record.product_uom_qty != 0:
                    record.pc_bulto = math.floor(record.product_uom_qty / float(record.product_id.x_pcsbulto))
                else:
                    record.pc_bulto = 0

                if record.product_id.x_pcpackage and record.product_id.x_pcpackage.isnumeric() and float(record.product_id.x_pcpackage) != 0 and record.product_uom_qty != 0:
                    record.pc_package = math.floor(record.product_uom_qty / float(record.product_id.x_pcpackage))
                else:
                    record.pc_package = 0

                if record.product_id.x_pacbulto and record.product_id.x_pacbulto.isnumeric() and float(record.product_id.x_pacbulto) != 0 and record.product_uom_qty != 0:
                    record.pck_bulto = math.floor(record.pc_package / float(record.product_id.x_pacbulto))
                else:
                    record.pck_bulto = 0