# -*- coding: utf-8 -*-
{
    'name' : 'Alsalem Contract',
    'version' : '1.1.0',
    'summary': "Kb Alsalem Contracts",
    'sequence': 15,
    'author': 'Knowledge Bonds',
    'maintainer': 'Knowledge Bonds',
    'website': '',

    'depends': ['hr'],
    'data': [
            'security/ir.model.access.csv',
            'data/data.xml',
            'views/contract_info_view.xml',
            'views/hr_employee.xml',
            'views/contract_report.xml',
            ],
    'demo': [],
    'license': 'OPL-1',
    'qweb': [],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}