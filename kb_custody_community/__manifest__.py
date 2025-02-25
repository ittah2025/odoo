# -*- coding: utf-8 -*-
{
    'name': 'KB Custody',
    'version': '16.1.0',
    'summary': "Concrete",
    'description': """
                This Is Custody Module 
                    """,
    'author': 'Knowledge Bonds, Ahmed Abutalib',
    'maintainer': 'Knowledge Bonds',
    'website': '',
    'depends': ['base', 'mail', 'hr', 'om_account_asset'],
    'data': [
        "data/kb_custody_seq.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/hr_custody.xml",
        "views/account_asset_view.xml",
        "views/hr_employee_view.xml",
        "views/asset_type_view.xml",
        "reports/custody_template.xml",

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
