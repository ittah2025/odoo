import datetime
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.tools.float_utils import float_round
from odoo.addons.resource.models.resource import HOURS_PER_DAY


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    # current_leave_state = fields.Selection(compute='_compute_leave_status', string="Current Time Off Status",
    #     selection=[
    #         ('draft', 'New'),
    #         ('confirm', 'Waiting Approval'),
    #         ('refuse', 'Refused'),
    #         ('validate1', 'Waiting Second Approval'),
    #         ('validate', 'Approved'),
    #         ('cancel', 'Cancelled')
    #     ])
    
    current_leave_state = fields.Selection(selection_add=[('additional_validate', 'Second Approval'),])