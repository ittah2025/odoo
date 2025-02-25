from odoo import api, fields, models


class HrContract(models.Model):
    """
    Employee contract based on the visa, work permits
    allows to configure different Salary structure
    """
    _inherit = 'hr.contract'

    kb_assignment_allowance = fields.Monetary(string="Assignment allowance", help="Enter assignment_allowance")
    kb_overtime_allowance = fields.Monetary(string="Overtime allowance", help="Enter overtime_allowance")
