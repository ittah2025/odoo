from odoo import fields, models


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    include_weekends = fields.Boolean(
    string='Exclude Weekends', 
    default=True,
    help=('If checked, time-off will dependent on Working Hours. \n If unchecked, weekends will be included in time-off.'))