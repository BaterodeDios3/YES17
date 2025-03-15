from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #metodo que cuando se cambie pricelist_id se actualice el campo price_unit de order_line
    @api.onchange('pricelist_id')
    def _onchange_pricelist_id(self):
        for line in self.order_line:
            now = fields.Datetime.now()
            LisProduct = self.pricelist_id.item_ids.filtered(lambda r: r.product_tmpl_id.id == line.product_id.product_tmpl_id.id)
            filterSorted = LisProduct.sorted(key=lambda r: r.min_quantity)
            if LisProduct:
                for list_id in filterSorted:
                    if line.product_id.product_tmpl_id.id == list_id.product_tmpl_id.id:
                        if line.product_uom_qty >= list_id.min_quantity and (not list_id.date_start or list_id.date_start <= now) and (not list_id.date_end or list_id.date_end >= now):
                            line.price_unit = list_id.fixed_price
            else:
                line.price_unit = line.product_id.lst_price

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    #metodo que cuando se cambie product_id se actualice el campo price_unit
    @api.onchange('product_id')
    def _onchange_product_id(self):
        now = fields.Datetime.now()
        LisProduct = self.order_id.pricelist_id.item_ids.filtered(lambda r: r.product_tmpl_id.id == self.product_id.product_tmpl_id.id)
        filterSorted = LisProduct.sorted(key=lambda r: r.min_quantity)
        if LisProduct:
            for list_id in filterSorted:
                if self.product_id.product_tmpl_id.id == list_id.product_tmpl_id.id:
                    if self.product_uom_qty >= list_id.min_quantity and (not list_id.date_start or list_id.date_start <= now) and (not list_id.date_end or list_id.date_end >= now):
                        self.price_unit = list_id.fixed_price
        else:
            self.price_unit = self.product_id.lst_price

    #metodo que cuando se cambie product_uom_qty se actualice el campo price_unit
    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
        now = fields.Datetime.now()
        LisProduct = self.order_id.pricelist_id.item_ids.filtered(lambda r: r.product_tmpl_id.id == self.product_id.product_tmpl_id.id)
        filterSorted = LisProduct.sorted(key=lambda r: r.min_quantity)
        if LisProduct:
            for list_id in filterSorted:
                if self.product_id.product_tmpl_id.id == list_id.product_tmpl_id.id:
                    if self.product_uom_qty >= list_id.min_quantity and (not list_id.date_start or list_id.date_start <= now) and (not list_id.date_end or list_id.date_end >= now):
                        self.price_unit = list_id.fixed_price
        else:
            self.price_unit = self.product_id.lst_price


    @api.model
    def create(self, vals):
        """Sobrescribir create para actualizar price_unit solo si es necesario."""
        record = super(SaleOrderLine, self).create(vals)
        if 'product_id' in vals:
            record._onchange_product_id()
        if 'product_uom_qty' in vals:
            record._onchange_product_uom_qty()
        return record


    def write(self, vals):
        """Sobrescribir write para actualizar price_unit solo si product_id o product_uom_qty cambian."""
        res = super(SaleOrderLine, self).write(vals)
        if 'product_id' in vals:
            for line in self:
                line._onchange_product_id()
        if 'product_uom_qty' in vals:
            for line in self:
                line._onchange_product_uom_qty()
        return res
