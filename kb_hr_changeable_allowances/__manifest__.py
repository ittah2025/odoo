{
    "name": "Changeable Allowances",
    "version": "16.0.0",
    "sequence": 15,
    "category": "Accounting",
    "summary": "Changeable Allowances",
    "license": "OPL-1",
    "description": """
            Changeable Allowances 
                """,
    "author": "Knowledge Bonds",
    "maintainer": "Knowledge Bonds",
    "website": "https://www.knowledge-bonds.com/en/",
    "depends": [
        "base",
        "hr_payroll_community",  #  Cybrosys Techno solutions , Open HRMS
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_contract_views.xml",
        "data/hr_payroll_data.xml",
        "wizard/changeable_allowance.xml",
    ],
    "qweb": [],
    "images": ["static/description/icon.png"],
    "installable": True,
    "application": True,
    "auto_install": False,
}
