from odoo import fields, models
from odoo import _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError


class test(models.TransientModel):

    _name = "kb_test"
    _description = "test report"

    def print_kb_trip_money_levels(self):

     return self.env.ref('kb_test.template_test_reprt_view').report_action(self)
