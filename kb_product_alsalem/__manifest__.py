{
    'name': 'Product AlSalem',
    'version': '14.0.0',
    'author': 'Knowledge bonds',
    'website': 'knowledge-bonds.com',
    'category': 'HR',
    "depends": ['sale_management','hr','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_fields.xml',
    ],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
    'qweb': [],
    'application': True,
}
