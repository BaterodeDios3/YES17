# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Product Restriction for Create/Update, Odoo Product Access Control Restrict',
    'version': '17.0.1.0',
    'sequence': 1,
    'category': 'Generic Modules/Sales Management',
    'description':
        """
        This Module add below functionality into odoo

        1.Only user with "Allow Create/Update/Delete Products" right can Create or Update or Delete Products\n
        2.Only user with "Allow Create/Update/Delete Products" right can Create or Update or Delete Product Variants\n
        
        
        Odoo Product Restriction
Create/Update Product Restrictions in Odoo
Odoo Product Access Control
Product Restriction Module in Odoo
Odoo Product Management Restrictions
Product Editing Restrictions in Odoo
Odoo Product Update Permissions
Odoo Product Modification Restrictions
Restricting Product Creation/Editing in Odoo
Product Security Restrictions in Odoo
Odoo Product Authorization Settings
Managing Product Restrictions in Odoo
Odoo Product Visibility Control
Odoo Product Editing Permissions
Odoo Product Modification Policies

odoo app control Create/Update Product Restrictions in Odoo,Odoo Product Access Control,Odoo Product Restriction,Create/Update/Delete Products,    Restriction on product create/delete,Product Editing Permissions,Product Security Restrictions in Odoo 

    """,
    'summary': 'odoo app control Create/Update Product Restrictions in Odoo,Odoo Product Access Control,Odoo Product Restriction,Create/Update/Delete Products,    Restriction on product create/delete,Product Editing Permissions,Product Security Restrictions in Odoo  ',
    'depends': ['product','sale_management'],
    'data': ['security/security.xml'],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    # author and support Details =============#
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':3.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
    'pre_init_hook' :'pre_init_check',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
