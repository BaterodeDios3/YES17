# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "Read Only Unit Price for Sales User",
    "version" : "17.0.0.0",
    "category" : "Sales",
    'summary': 'Read Only Unit Price for Sales Users sale price access sale price read only for sales user read only unit price for sales own document group sale order line unit price access read only unit price for sales person read only price unit read only on sale line',
    "description": """
    
        Read Only Unit Price for Sales User in odoo,
        Not Editable Unit Price for Sales User in odoo,
        Read Only Unit Price for Own Documents Only group in odoo,
        Read Only Unit Price for All Documents group in odoo,
        Editable Unit Price only for sales administrator user in odoo,
        Unit Price field should be Read Only for Sales User in odoo,
    
    """,
    "author": "BROWSEINFO",
    "price": 10,
    "currency": 'EUR',
    'website': 'https://www.browseinfo.com/demo-request?app=restrict_sales_user_app&version=17&edition=Community',
    "depends" : ['base','sale_management'],
    "data": [
        'views/view_sale_order_line.xml',
    ],
    'license': 'OPL-1',
    "auto_install": False,
    "installable": True,
    "live_test_url":'https://www.browseinfo.com/demo-request?app=restrict_sales_user_app&version=17&edition=Community',
    "images":["static/description/Banner.gif"],
}

