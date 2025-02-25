from odoo import models, fields, api


class HrLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    @api.depends('employee_id', 'holiday_status_id')
    def _compute_leaves(self):
        for allocation in self:
            leave_type = allocation.holiday_status_id.with_context(employee_id=allocation.employee_id.id)
            allocation.max_leaves = leave_type.max_leaves
            allocation.leaves_taken = leave_type.leaves_taken

    @api.model
    def get_alloctions(self):
        user_id = self.env.user.id
        allocation_records = self.search([
            ('employee_id.user_id', '=', user_id),
            ('state', '=', 'validate')
        ])
        # print('allocation_records', allocation_records)

        total_balance = self.env.user.employee_id.allocation_display
        remaining_balance = self.env.user.employee_id.allocation_remaining_display

        # print('ttl', total_balance, '|', remaining_balance)

        return {
            'total_balance': total_balance,
            'remaining_balance': remaining_balance,
            'allocations': [{
                'holiday_status_id': record.holiday_status_id.name,
                'max_leaves': int(record.max_leaves),
                'leaves_taken': int(record.leaves_taken),
            } for record in allocation_records]
        }
