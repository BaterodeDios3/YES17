# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


{
    'name': 'POS Analytic Account - POS Analytic Tags',
    'version': '17.0.0.0',
    'category': 'Point of Sale',
    'summary': 'Point of Sale Analytic account point of sale analytic tag on pos analytic account on pos analytic distribution on point of sales analytic distribution on pos analytic entry from the point of sale analytic entry pos cost center on point of sale cost centers',
    'description': """
    
          POS Analytic Tags with Distribution in odoo,
          POS Analytic Tags in odoo,
          POS Session with Custom Analytic Tags in odoo,
          POS Session Without Custom Analytic Tags in odoo,
          POS Session with Analytic Account in odoo,
          Configure Analytic Account in odoo,

    """,
    'author': 'BROWSEINFO',
    "price": 15,
    "currency": 'EUR',
    'website': "https://www.browseinfo.com/demo-request?app=bi_pos_analytic_tags&version=17&edition=Community",
    'depends': ['base','point_of_sale'],
    'data': [
        'views/point_of_sale.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            "bi_pos_analytic_tags/static/src/app/models.js",
            "bi_pos_analytic_tags/static/src/app/pos_store.js",
            "bi_pos_analytic_tags/static/src/app/PaymentScreen.js",
        ],
    },

    "license": "OPL-1",
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'live_test_url': 'https://www.browseinfo.com/demo-request?app=bi_pos_analytic_tags&version=17&edition=Community',
    "images": ['static/description/Banner.gif'],
}
