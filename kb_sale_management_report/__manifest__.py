{
    'name': 'Sale Management Report',
    'version': '1.0',
    'summary': 'Generate PDF reports for Sale Management',
    'author': 'kb',
    'category': 'Sales',
    'depends': ['base', 'kb_shareholder_management'],
    'data': [
        # 'views/sale_management_views.xml',
        'report/sale_management_report.xml',
    ],
    'installable': True,
    'application': False,
}
