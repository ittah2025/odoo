# Copyright 2015 2011,2013 Michael Telahun Makonnen <mmakonnen@gmail.com>
# Copyright 2020 InitOS Gmbh
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "HR Holidays Public",
    "version": "16.0.2.0.0",
    "license": "AGPL-3",
    "category": "Human Resources",
    "author": "Michael Telahun Makonnen, "
    "Tecnativa, "
    "Fekete Mihai (Forest and Biomass Services Romania), "
    "Druidoo, "
    "Odoo Community Association (OCA),",
    "summary": "Manage Public Holidays",
    "website": "https://github.com/OCA/hr-holidays",
    "depends": ["hr_holidays"],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "views/hr_holidays_public_view.xml",
        "views/hr_leave_type.xml",
        "wizards/holidays_public_next_year_wizard.xml",
    ],
    "installable": True,
}
