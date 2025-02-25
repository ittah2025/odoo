{
    'name': 'kb PR PO Levels',
    'version': '16.0.0',
    'category': 'purchae',
    'summary': "kb PR PO approval Levels",
    'description': """Purchase Requests""",
    'sequence': '18',
    'license': 'LGPL-3',
    'company': 'Knowledge Bonds',
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'depends': ['base','mail','purchase', 'stock', 'stock_analytic', 'multi_branch_base','account'],
    'demo': [],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        "wizard/purchase_request_line_make_purchase_order_view.xml",
        'views/pr_level.xml',
        'views/purchase_order.xml',
        'views/stock_picking.xml',
        'data/data_seq.xml',
        'views/payment_request.xml',

        
    ],

    'assets': {
    'web.assets_backend': [
        ],
        'web.assets_qweb': [
        ],
    },

    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'qweb': [],
}
