# pos_upinn_18/__manifest__.py
{
    'name': 'Stock Upinn 17',
    "author": "Alex Martínez",
    "website": "www.linkedin.com/in/baterodedios",
    'version': '1.0',
    'category': 'stock',
    'summary': 'Stock personaliado para Upinn 17',
    'depends': ['stock','product','point_of_sale'],
    'data': [
        'views/stock_quants_views.xml',
        'security/groups.xml',
    ],
    "assets": {
        "point_of_sale.assets_prod": [
            "stock_uppin_17/static/src/app/screens/product_info_popup.js",
            "stock_uppin_17/static/src/app/screens/product_info_popup.xml",
        ],
    },
    'installable': True,
    'application': False,
}
