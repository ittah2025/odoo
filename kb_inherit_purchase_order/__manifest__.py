{
    'name': 'Xpath Requests For Quotation',
    'version': '16.0',
    'currency': 'SAR',
    'website': 'http://www.knowledge-bonds.com',
    'support': 'info@knowledge-bonds.com',
    'author': 'Knowledge Bonds',
    "depends": ['purchase'],
    'license': 'OPL-1',
    'sequence': 20,
    'data': [
        'security/ir.model.access.csv',
        'views/kb_xpath_requests_for_quotation.xml',
    ],
    'images': ['static/description/icon.png'],
    'application': True,
}
