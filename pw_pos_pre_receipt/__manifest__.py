# -*- coding: utf-8 -*-
{
    'name': 'POS PreSale Receipt',
    'version': '1.0',
    'category': 'Point Of Sale',
    'author': 'Preway IT Solutions',
    'summary': 'This apps allow you to print pos order receipt before payment | POS Quick Receipt | POS Presale Receipt | POS Receipt Preview | POS Quick Print Receipt | Point Of Sale Quick Print Receipt',
    'description': """
This apps helps you to print pos receipt before order.
""",
    'depends': ['point_of_sale'],
    'data': [
        'views/res_config_settings_view.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            # 'pw_pos_pre_receipt/static/src/js/models.js',
            'pw_pos_pre_receipt/static/src/js/ReceiptReviewButton.js',
            'pw_pos_pre_receipt/static/src/js/ReceiptScreen.js',
            'pw_pos_pre_receipt/static/src/xml/main.xml',
        ],
    },
    'price': 30.0,
    'currency': 'EUR',
    'installable': True,
    'application': True,
    "license": "LGPL-3",
    "images":["static/description/Banner.png"],
}
