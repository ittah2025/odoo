from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, date, time


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)', tracking=True,
        groups="base.group_user")

    identification_id = fields.Char(string='Identification No', groups="base.group_user", tracking=True)

    birthday = fields.Date('Date of Birth', groups="base.group_user", tracking=True)

    barcode = fields.Char(string="Badge ID", help="ID used for employee identification.", groups="base.group_user", copy=False)

    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', groups="base.group_user", default='single', tracking=True)

    first_contract_date = fields.Date(compute='_compute_first_contract_date', groups="base.group_user", store=True)

    passport_id = fields.Char('Passport No', groups="base.group_user", tracking=True)

    address_home_id = fields.Many2one(
        'res.partner', 'Address',
        help='Enter here the private address of the employee, not the one linked to your company.',
        groups="base.group_user", tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    @api.model
    def create_loan(self,loans):
        employee = self.env['hr.employee'].sudo().search([('user_id','=', self.env.user.id)])
        loan_boolean = False
        if loans[0] and loans[1] and loans[2]:
            loan_id = self.env['hr.loan'].sudo().create([{
                'employee_id': employee.id,
                'date': date.today(),
                'loan_amount': loans[0],
                'installment': loans[1],
                'payment_date': loans[2],
            }])
            if loan_id:
                loan_id.compute_installment()
                loan_boolean = True

        data = {
            'employee': employee,
            'loan_boolean': loan_boolean,
        }
        return data

    @api.model
    def createResignation(self,resignation):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if resignation[0] and resignation[1]:
            resignation_id = self.env['hr.resignation'].sudo().create([{
                'employee_id': employee.id,
                'expected_revealing_date': resignation[0],
                'reason': resignation[1],
            }])

        data = {
            'employee': employee,
        }
        return data


    @api.model
    def create_training(self, training):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        resignation_id = self.env['kb.training.request'].sudo().create([{
            'name': training[0],
            'employee_id': employee.id,
            'date_from': training[1],
            'date_to': training[2],
            'source': training[3],
            'place': training[4],
        }])

        data = {
            'employee': employee,
        }
        return data

    @api.model
    def get_all_partners(self):
        partners = self.env['res.partner'].sudo().search([])
        partner_data = []
        for partner in partners:
            partner_data.append({
                'id': partner.id,
                'name': partner.name
            })
        return partner_data

    @api.model
    def get_all_users(self):
        users = self.env['res.users'].sudo().search([])
        user_data = []
        for user in users:
            user_data.append({
                'id': user.id,
                'name': user.name
            })
        return user_data

    @api.model
    def get_all_project(self):
        projects = self.env['project.project'].sudo().search([])
        project_data = []
        for project in projects:
            project_data.append({
                'id': project.id,
                'name': project.name
            })
        return project_data

    @api.model
    def create_meeting(self, listbox, meeting):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        print(meeting)
        partner = []
        for rec in listbox:
            partner.append(int(rec))
        # print("users")
        strdate_obj = datetime.strptime(meeting[1], '%Y-%m-%d')
        start_year = strdate_obj.year
        start_month = strdate_obj.month
        start_day = strdate_obj.day
        enddate_obj = datetime.strptime(meeting[3], '%Y-%m-%d')
        end_year = enddate_obj.year
        end_month = enddate_obj.month
        end_day = enddate_obj.day

        sub_str = ":"
        strhor = meeting[2][:meeting[2].index(sub_str) + (len(sub_str) - 1)]
        strmin = meeting[2][meeting[2].rindex(sub_str) + 1:]
        strhorx = int(strhor)
        strminx = int(strmin)
        strMyDate = date(int(start_year), int(start_month), int(start_day))
        strMyTime = time(strhorx, strminx)
        strdatetime = datetime.combine(strMyDate, strMyTime)

        endhor = meeting[4][:meeting[4].index(sub_str) + (len(sub_str) - 1)]
        endmin = meeting[4][meeting[4].rindex(sub_str) + 1:]
        endhorx = int(endhor)
        endminx = int(endmin)
        endMyDate = date(int(end_year), int(end_month), int(end_day))
        endMyTime = time(endhorx, endminx)
        enddatetime = datetime.combine(endMyDate, endMyTime)

        # print(meeting[1], meeting[2])
        event_id = self.env['calendar.event'].sudo().create([{
            'user_id': self.env.user.id,
            'start': strdatetime,
            'stop': enddatetime,
            'partner_ids': [(6, 0, partner)],
            'name': meeting[0],
        }])
        # print(event_id)
        data = {
            'employee': employee,
        }
        return data

    @api.model
    def create_task(self, txt,tasking):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        users = []
        for rec in txt:
            users.append(int(rec))
        print("users")
        print(users)
        task_id = self.env['project.task'].sudo().create([{
            'project_id': int(tasking[2]),
            'user_ids': [(6, 0, users)],
            'name': tasking[0],
        }])
        print(task_id)
        data = {
            'employee': employee,
        }
        return data






    @api.model
    def get_data(self):
        employee = self.env['hr.employee'].sudo().search([('id', '=', self.env.user.employee_id.id)], limit=1)
        contract_record = self.env['hr.contract'].sudo().search([('employee_id.user_id', '=', self.env.user.id)],
                                                                limit=1)
        payslip_count = self.env['hr.payslip'].sudo().search_count([('employee_id.user_id', '=', self.env.user.id)])
        contract_count = self.env['hr.contract'].sudo().search_count([('employee_id.user_id', '=', self.env.user.id)])
        task_count = self.env['project.task'].sudo().search_count([('user_ids', '=', self.env.user.id)])
        ticket_count = self.env['help.ticket'].sudo().search_count([('assigned_user', '=', self.env.user.id)])



        if employee:
            id = employee.id
            name = employee.name
            job = employee.job_id.name if employee.job_id else ''
            department = employee.department_id.name if employee.department_id else ''
            parent_id = employee.parent_id.name if employee.parent_id else ''
            image = employee.image_1920
            allocation_display = employee.allocation_display
            allocation_remaining_display = employee.allocation_remaining_display
            payslip_count = payslip_count
            contract_count = contract_count
            task_count = task_count
            ticket_count = ticket_count
            contract_name = contract_record.name if contract_record else ''
            user_id = employee.user_id.id if employee.user_id else None
            # allocation = allocation.holiday_status_id

            return {
                'employee': {
                    'id': id,
                    'name': name,
                    'job': job,
                    'department': department,
                    'parent_id': parent_id,
                    'image': image,
                    'payslip_count': payslip_count,
                    'allocation_display': allocation_display,
                    'allocation_remaining_display': allocation_remaining_display,
                    'contract_count': contract_count,
                    'task_count': task_count,
                    'ticket_count': ticket_count,
                    'contract_name': contract_name,
                    'user_id': user_id
                }
            }

        else:
            print('Employee not found for the current user')
            raise UserError('Employee not found for the current user')


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'


class HrContract(models.Model):
    _inherit = 'hr.contract'

    @api.model
    def get_contract_data(self):
        contract = self.env['hr.contract'].sudo().search([('employee_id.user_id', '=', self.env.user.id)], limit=1)
        print('contract', contract.job_id.name)
        if contract:
            id = contract.id
            name = contract.name
            date_start = contract.date_start
            date_end = contract.date_end
            department_id = contract.department_id
            job_id = contract.job_id.name

            return {
                'employee': {
                    'id': id,
                    'name': name,
                    'date_start': date_start,
                    'date_end': date_end,
                    'department_id': department_id,
                    'job_id': job_id,
                }
            }
        else:
            print('Contract not found for the current user')
            return {}


class HrPayslipWorkedDays(models.Model):
    _inherit = 'hr.payslip.worked_days'


class HrPayslipInput(models.Model):
    _inherit = 'hr.payslip.input'


class HrPayslipInput(models.Model):
    _inherit = 'hr.payslip.line'


class Job(models.Model):
    _inherit = 'hr.job'
