import logging
import pytz

from collections import namedtuple, defaultdict

from datetime import datetime, timedelta, time
from pytz import timezone, UTC
from odoo.tools import date_utils

from odoo import api, Command, fields, models, tools
from odoo.addons.base.models.res_partner import _tz_get
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_compare
from odoo.tools.float_utils import float_round
from odoo.tools.misc import format_date
from odoo.tools.translate import _
from odoo.osv import expression


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    state = fields.Selection([
        ('draft', 'To Submit'),
        ('confirm', 'To Approve'),
        ('refuse', 'Refused'),
        ('additional_validate', 'Second Approval'),
        ('validate1', 'Third Approval'),
        ('validate', 'Approved')
        ], string='Status', compute='_compute_state', store=True, tracking=True, copy=False, readonly=False,
        help="The status is set to 'To Submit', when a time off request is created." +
        "\nThe status is 'To Approve', when time off request is confirmed by user." +
        "\nThe status is 'Refused', when time off request is refused by manager." +
        "\nThe status is 'Approved', when time off request is approved by manager.")


    def _check_approvals(self) -> dict:
        users = self.env['res.users'].search([])
        all_approval_users = {
            "second_approval": [user.id for user in users if user.has_group('kb_holiday_approvals_updation.group_additional_holiday_administrator')],
            "current_userid": str(self.env.uid),
            }
        print ("all_approval_users",all_approval_users)
        return all_approval_users

    def action_addtional_approval(self):
        group_expense_third_approval = self.env.user.has_group('kb_holiday_approvals_updation.group_additional_holiday_administrator')
        if group_expense_third_approval:
            self.write({'state': 'validate1'})
        else:
            raise AccessError(_("You don't have access rights to this action."))


    def action_approve(self):
        # if validation_type == 'both': this method is the first approval approval
        # if validation_type != 'both': this method calls action_validate() below

        # group_hr_holidays_administrator = self.env.user.has_group('hr_holidays.group_hr_holidays_manager')
        # group_hr_holidays_user = self.env.user.has_group('hr_holidays.group_hr_holidays_user')
        # if group_hr_holidays_administrator or group_hr_holidays_user or self.employee_id.leave_manager_id:

        if any(holiday.state != 'confirm' for holiday in self):
            raise UserError(_('Time off request must be confirmed ("To Approve") in order to approve it.'))

        current_employee = self.env.user.employee_id
        employee = self.employee_ids.country_id.id
        print ('employeeemployee',employee)
        if employee == 192:
            self.filtered(lambda hol: hol.validation_type == 'both').write({'state': 'validate1', 'first_approver_id': current_employee.id})
        else:
            self.filtered(lambda hol: hol.validation_type == 'both').write({'state': 'additional_validate', 'first_approver_id': current_employee.id})
            approval_list = self._check_approvals().get("second_approval")
            for second_approval in approval_list:
                self.activity_schedule('hr_holidays.mail_act_leave_approval', 
                                    user_id=second_approval, 
                                    note=f'New {self.holiday_status_id.name}s Request created by {self.create_uid.name}s',) # date_deadline=deadline_in1d


        # Post a second message, more verbose than the tracking message
        for holiday in self.filtered(lambda holiday: holiday.employee_id.user_id):
            user_tz = timezone(holiday.tz)
            utc_tz = pytz.utc.localize(holiday.date_from).astimezone(user_tz)
            holiday.message_post(
                body=_(
                    'Your %(leave_type)s planned on %(date)s has been accepted',
                    leave_type=holiday.holiday_status_id.display_name,
                    date=utc_tz.replace(tzinfo=None)
                ),
                partner_ids=holiday.employee_id.user_id.partner_id.ids)

        self.filtered(lambda hol: not hol.validation_type == 'both').action_validate()
        if not self.env.context.get('leave_fast_create'):
            self.activity_update()
        return True
        # else: raise AccessError(_("You don't have access rights to this action."))

    def _check_approval_update(self, state):
        """ Check if target state is achievable. """
        if self.env.is_superuser():
            return

        current_employee = self.env.user.employee_id
        is_officer = self.env.user.has_group('hr_holidays.group_hr_holidays_user')
        is_manager = self.env.user.has_group('hr_holidays.group_hr_holidays_manager')

        for holiday in self:
            val_type = holiday.validation_type

            if not is_manager and state != 'confirm':
                if state == 'draft':
                    if holiday.state == 'refuse':
                        raise UserError(_('Only a Time Off Manager can reset a refused leave.'))
                    if holiday.date_from and holiday.date_from.date() <= fields.Date.today():
                        raise UserError(_('Only a Time Off Manager can reset a started leave.'))
                    if holiday.employee_id != current_employee:
                        raise UserError(_('Only a Time Off Manager can reset other people leaves.'))
                else:
                    if val_type == 'no_validation' and current_employee == holiday.employee_id:
                        continue
                    # use ir.rule based first access check: department, members, ... (see security.xml)
                    holiday.check_access_rule('write')

                    # This handles states validate1 validate and refuse
                    if holiday.employee_id == current_employee:
                        raise UserError(_('Only a Time Off Manager can approve/refuse its own requests.'))

                    if (state == 'validate1' and val_type == 'both') and holiday.holiday_type == 'employee':
                        group_expense_second_approval = self.env.user.has_group('kb_holiday_approvals_updation.group_additional_holiday_administrator')
                        if not is_officer and self.env.user != holiday.employee_id.leave_manager_id and not group_expense_second_approval:
                            raise UserError(_('You must be either %s\'s manager or Time off Manager to approve this leave') % (holiday.employee_id.name))

                    if (state == 'validate' and val_type == 'manager') and self.env.user != holiday.employee_id.leave_manager_id:
                        raise UserError(_('You must be %s\'s Manager to approve this leave', holiday.employee_id.name))

                    if not is_officer and (state == 'validate' and val_type == 'hr') and holiday.holiday_type == 'employee':
                        raise UserError(_('You must either be a Time off Officer or Time off Manager to approve this leave'))


    def _check_double_validation_rules(self, employees, state):
        if self.user_has_groups('hr_holidays.group_hr_holidays_manager') or self.user_has_groups('kb_holiday_approvals_updation.group_additional_holiday_administrator'):
            return

        is_leave_user = self.user_has_groups('hr_holidays.group_hr_holidays_user')
        if state == 'validate1':
            employees = employees.filtered(lambda employee: employee.leave_manager_id != self.env.user)
            if employees and not is_leave_user:
                raise AccessError(_('You cannot first approve a time off for %s, because you are not his time off manager', employees[0].name))
        elif state == 'validate' and not is_leave_user:
            # Is probably handled via ir.rule
            raise AccessError(_('You don\'t have the rights to apply second approval on a time off request'))


    # @api.model
    # def search(self, args, offset=0, limit=None, order=None, count=False):
    #     user = self.env.user
    #     if user.has_group('base.group_system'):
    #         # User is admin, return all tasks
    #         print('22222222',args)
    #         return super(HrLeave, self).search(args, offset, limit, order, count=count)
    #     elif user.has_group('kb_holiday_approvals_updation.group_additional_holiday_administrator'):
    #         # User is a regular user, return only their own tasks
    #         # args.append(('user_id', '=', user.id))
    #         print('33333333',args)
    #         return super(HrLeave, self).search(args, offset, limit, order, count=count)
        



