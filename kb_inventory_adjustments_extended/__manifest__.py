{
    'name': 'KB Inventory Adjustments Extended',
    'version': '16.0.0.1',
    'summary': 'KB Inventory Adjustments Extended',
    'description': 'KB Inventory Adjustments Extended',
    'category': 'Services',
    'author': 'Knowledge bonds',
    'website': 'https://knowledge-bonds.com/',
    'maintainer': 'Knowledge bonds',
    'license': 'OPL-1',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/kb_inventory_adjustments_extended_wizard.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'auto_install': False,
}
