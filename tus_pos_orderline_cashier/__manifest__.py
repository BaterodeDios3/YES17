# -*- coding: utf-8 -*-
{
    # App information
    'name': 'Odoo POS Orderline Cashier',
    'version': '17.0.0.1',
    'summary': 'POS Orderline Cashier',
    'category': 'Point Of Sale',
    'author': 'TechUltra Solutions Private Limited',
    'license': 'OPL-1',
    'company': 'TechUltra Solutions Private Limited',
    'website': 'https://www.techultrasolutions.com/',

    # Dependencies
    'depends': ['point_of_sale', 'pos_hr'],

    # Data
    'data': [
        'views/pos_config_views.xml',
        'views/pos_order_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'tus_pos_orderline_cashier/static/src/app/cashier_button/cashier.xml',
            'tus_pos_orderline_cashier/static/src/app/cashier_button/orderline.xml',
            'tus_pos_orderline_cashier/static/src/overrides/models/model.js',
            'tus_pos_orderline_cashier/static/src/overrides/orderrecipt.js',
            'tus_pos_orderline_cashier/static/src/app/cashier_button/cashier.js',
            'tus_pos_orderline_cashier/static/src/app/cashier_button/orderline.js',
            'tus_pos_orderline_cashier/static/src/app/cashier_button/pos_load_hr_employe.js',
        ],
    },

    # Images
    'images': [
        #'static/description/icon.png',
    ],

    # Technical
    'price': 13,
    'currency': 'USD',
    'installable': True,
    'application': True,
    'auto_install': False,
}
