
from odoo import models, fields, api, _


class OrderReportLine(models.Model):
    _inherit = "pos.order.line"

    cost_price = fields.Float(related='product_id.standard_price', store=True)
    sale_price = fields.Float(related='product_id.lst_price', store=True)

class PosOrderReport(models.Model):
    _inherit = "report.pos.order"

    cost_price = fields.Float('Cost Price/Unit')
    cost_price_total = fields.Float('Cost Price Total')
    sale_price = fields.Float('Profit(Sale Price - Cost Price)')
    sale_price_total = fields.Float('Total Profit(Total Sales - Total Cost')


    def _select(self):
        return super(PosOrderReport, self)._select() + ',sum(l.cost_price) / COUNT(l.id) AS cost_price, ' \
                                                       'sum(l.cost_price) * sum(l.qty) AS cost_price_total, ' \
                                                       'sum(l.sale_price) - sum(l.cost_price) AS sale_price, ' \
                                                       '(sum(l.sale_price) - sum(l.cost_price)) * sum(l.qty) AS sale_price_total'

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        res = super(PosOrderReport, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        for record in res:
            if record.get('cost_price'):
                record['cost_price'] = record.get('cost_price')/record.get('__count')
            if record.get('sale_price'):
                record['sale_price'] = record.get('sale_price')/record.get('__count')
        return res
