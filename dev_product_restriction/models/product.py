# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def restrict_user(self):
        raise ValidationError("You are not allowed to Create/Update/Delete Products")

    @api.model
    def create(self, values):
        res = super(ProductTemplate, self).create(values)
        if not self.env.user.has_group('dev_product_restriction.can_modify_products'):
            self.restrict_user()
        return res

    def write(self, values):
        res = super(ProductTemplate, self).write(values)
        if not self.env.user.has_group('dev_product_restriction.can_modify_products'):
            self.restrict_user()
        return res

    def unlink(self):
        res = super(ProductTemplate, self).unlink()
        if not self.env.user.has_group('dev_product_restriction.can_modify_products'):
            self.restrict_user()
        return res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def restrict_user(self):
        raise ValidationError("You are not allowed to Create/Update/Delete Products")

    @api.model
    def create(self, values):
        res = super(ProductProduct, self).create(values)
        if not self.env.user.has_group('dev_product_restriction.can_modify_products'):
            self.restrict_user()
        return res

    def write(self, values):
        res = super(ProductProduct, self).write(values)
        if not self.env.user.has_group('dev_product_restriction.can_modify_products'):
            self.restrict_user()
        return res

    def unlink(self):
        res = super(ProductProduct, self).unlink()
        if not self.env.user.has_group('dev_product_restriction.can_modify_products'):
            self.restrict_user()
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: