{
    'name': 'Move Year',
    'version': '14.0.0',
    'author': 'Knowledge bonds',
    'website': 'knowledge-bonds.com',
    'category': 'School Management',
    'summary': 'Move The student to next year',
    'description': """Move The student to next year""",
    'sequence': -99,
    'depends': ['kb_hr_tahtheeb'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/move_year_view.xml',
    ],
    'installable': True,
    'application': True
}
