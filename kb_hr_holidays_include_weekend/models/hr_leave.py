from odoo import models, api, _
from odoo.exceptions import AccessError, UserError, ValidationError

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.onchange('holiday_status_id')
    def recompute_no_days(self):
        self._compute_number_of_days()

    def _get_number_of_days(self, date_from, date_to, employee_id):
        context_data = {'employee_id' : employee_id,
                        'from_leave_request': True,
                        'include_weekends' : False}

        if (self.holiday_status_id.include_weekends or
                not self.holiday_status_id):
            context_data['include_weekends'] = True
        instance = self.with_context(context_data)
        # raise UserError(_('weekdays: {}'.format(context_data)))
        return super(HrLeave, instance)._get_number_of_days(
            date_from,
            date_to,
            employee_id,
        )
