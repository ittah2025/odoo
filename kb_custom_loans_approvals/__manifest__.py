# -*- coding: utf-8 -*-
{
    'name': 'kb_custom_loans_approvals',
    'version': '16.0.0',
    'sequence': 22,
    'author': 'Knowledge bonds',
    'website': 'knowledge-bonds.com',
    'category': 'Loans Approvals',
    'license': 'OPL-1',
    'author': 'Knowledge Bonds',
    'website': 'https://www.knowledge-bonds.com',
    'maintainer': 'Knowledge Bonds',
    'depends': ['base', 'hr','ohrms_loan','kb_employee_extra_info','hr_contract'],
    'data': [
        'security/security.xml',
        'views/views.xml',
        ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    "currency": "USD",
}
