from num2words import num2words
from odoo import api, fields, models, _
from datetime import datetime, date
from odoo.exceptions import ValidationError, UserError
import arabic_reshaper
from bidi.algorithm import get_display
import hijridate
from hijridate import Hijri, Gregorian

class HrFormReason(models.Model):
    _name = "kb.hr.forms.reason"
    _description = "HR Report"
    _rec_name = 'kb_reason'

    kb_reason = fields.Char(string='Reason')


class HrFormWizard(models.Model):
    _name = "kb.hr.forms.wizard"
    _description = "HR Reports"

    kb_reportType = fields.Selection([
        ('report1', 'إنهاء عقد'),
        ('report19', 'إبراء ذمة'),
        ('report8', 'تعريف الراتب'),
        ('report11', 'انهاء عقد مكتب التعليم'),
        ('report20', 'اتفاقية سرية المعلومات'),
        ('report12', 'انذار اساءة سلوك'),
        ('report13', 'انذار تاخير'),
        ('report4', 'تثبيت الراتب بنك الفرنسي'),
        ('report14', 'بيانات وظيفية لعقد'),
        ('report21', 'شهادة خبره واخلاء طرف'),
        ('report2', 'خطاب نقل موظف'),
        ('report16', 'خطاب تمديد'),
        ('report17', 'نموذج انهاء عقد 2024'),
        ('report22', 'عرض وظيفي - اداري'),
        ('report18', 'نموذج بيان الرغبة بالاستمرارية -1 2024 معتمد'),
        ('report15', 'تعديل راتب مسمى وظيفي'),
        ('report23', 'نموذج ساعات اضافية - مدارس'),
        ('report24', 'نموذج ساعات اضافية - ادارة'),
    ], string='Report')

    kb_employeeID = fields.Many2one('hr.employee', string='Employee Name', required=True)
    kb_reasonID = fields.Many2one('kb.hr.forms.reason', string='Reason')
    kb_date = fields.Date(string='Date', default=fields.Date.today(), store=True)
    kb_date_to = fields.Date(string='Date to')
    kb_responsible = fields.Many2one("res.users", string='Responsible', readonly=True,
                                     default=lambda self: self.env.user)
    kb_branchName = fields.Many2one("res.branch", string='Branch Name', default=False)
    to_branch = fields.Many2one("res.branch", string='To Branch Name', default=False)
    kb_branchNamesecond = fields.Many2one("res.branch", string='To Branch', default=False)
    kb_type_bank = fields.Selection([('bank1', 'بنك الأهلي'), ('bank2', 'بنك الفرنسي')], string='Bank')
    # kb_sender = fields.Char(string="Name of the sender")
    kb_employee_name = fields.Char(string='Employee Name', related='kb_employeeID.name')
    # kb_employee_name_2 = fields.Char(string='Employee Name')
    kb_employee_job = fields.Char(string='Job Title')
    weekday = fields.Selection([
        ('0', 'الاثنين'),
        ('1', 'الثلاثاء'),
        ('2', 'الاربعاء'),
        ('3', 'الخميس'),
        ('4', 'الجمعة'),
        ('5', 'السبت'),
        ('6', 'الاحد'),
    ], string="Weekday", compute='_compute_weekday', store=True)
    weekday_label = fields.Char(string="Weekday Label", compute='_compute_weekday_label', store=True)
    kb_salary = fields.Float(string='Salary', compute='get_kb_salary')
    kb_salary_words = fields.Char(string='Salary in Words', compute='_compute_salary_words', store=True)
    kb_basic_salary = fields.Float(string='Basic Salary')
    kb_housing_allowance = fields.Float(string='Housing Allowance')
    kb_transfer_allowance = fields.Float(string='Transfer Allowance')
    kb_special_conditions = fields.Boolean(string='Special Conditions')
    kb_special_conditions_2 = fields.Boolean(string='Special Conditions 2')
    kb_salary_2 = fields.Float(string='Salary Upgrade')
    kb_basic_salary_2 = fields.Float(string='Basic Salary 2')
    kb_housing_allowance_2 = fields.Float(string='Housing Allowance 2')
    kb_transfer_allowance_2 = fields.Float(string='Transfer Allowance 2')
    kb_basic_salary_in_words = fields.Char(string='Basic Salary in Words', compute='_compute_salary_words_2',
                                           store=True)
    location = fields.Char()
    holidays = fields.Integer()
    days_of_work = fields.Integer()
    insurance = fields.Char()
    arabic_date = fields.Char(string='Arabic Date')
    date = fields.Date(default=fields.Date.today(), store=True)
    job = fields.Char(string='About')
    content = fields.Char('Content')

    @api.depends('kb_basic_salary', 'kb_housing_allowance', 'kb_transfer_allowance')
    def get_kb_salary(self):
        for rec in self:
            if rec.kb_transfer_allowance and rec.kb_housing_allowance and rec.kb_basic_salary:
                rec.kb_salary = rec.kb_basic_salary + rec.kb_transfer_allowance + rec.kb_housing_allowance
            else:
                rec.kb_salary = 0

    @api.depends('kb_basic_salary_2')
    def _compute_salary_words_2(self):
        for record in self:
            if record.kb_basic_salary_2:
                record.kb_basic_salary_in_words = num2words(record.kb_basic_salary_2, lang='ar_001')
            else:
                record.kb_basic_salary_in_words = False

    @api.depends('kb_salary')
    def _compute_salary_words(self):
        for record in self:
            if record.kb_salary:
                record.kb_salary_words = num2words(record.kb_salary, lang='ar_001')
            else:
                record.kb_salary_words = False

    @api.depends('kb_date')
    def _compute_weekday(self):
        for record in self:
            if record.kb_date:
                weekday = fields.Date.from_string(record.kb_date).weekday()
                record.weekday = str(weekday)
            else:
                record.weekday = False

    @api.depends('weekday')
    def _compute_weekday_label(self):
        for record in self:
            if record.weekday:
                record.weekday_label = dict(record._fields['weekday'].selection).get(record.weekday)
            else:
                record.weekday_label = False

    def check_the_day_name(self):
        for record in self:
            weekday = fields.Date.from_string(fields.date.today()).weekday()
            weekday_label = dict(record._fields['weekday'].selection).get(record.weekday)
            return(weekday_label)
    def convert_to_hijri(self,kb_date_to):
        for r in self:
            return Gregorian(kb_date_to.year,kb_date_to.month,kb_date_to.day,).to_hijri()
    # This function fetches and retrieves all report data
    #######################################################
    def generate_report(self):
        for rec in self:
            # Call Report 1 'إنهاء عقد'
            if self.kb_reportType == 'report1':
                contract_list = []
                data = {
                    'form_data': self.read()[0],
                    'contractID': contract_list
                }
                company_id_here = self.env['res.company']._company_default_get('account.invoice')
                contract_id = self.env['hr.contract'].search([('employee_id','=',rec.kb_employeeID.id),('state','=','close')])
                if not contract_id:
                    raise UserError('لا يوجد عقد منتهي الصلاحية مرتبط  بالموظف')
                val = {
                    'gender':rec.kb_employeeID.gender,
                    'kb_employeeID': rec.kb_employeeID.name,
                    'kb_reasonID': rec.kb_reasonID.kb_reason,
                    'kb_date': contract_id.date_end,
                    'weekday_label':rec.weekday_label,
                    'kb_responsible': rec.kb_responsible.name,
                    'company_id_here': company_id_here.name,
                    'kb_branchName': rec.kb_branchName.name,
                }
                contract_list.append(val)
                return self.env.ref('kb_hr_tahtheeb.end_contract_reportID').report_action(self, data=data)
            # Call Report 2 'نقل موظف'
            elif self.kb_reportType == 'report2':
                employeeTransfer_list = []
                data = {
                    'form_data': self.read()[0],
                    'employeeTransferID': employeeTransfer_list
                }
                employeeInfo = self.env['hr.employee'].search([('name', '=', rec.kb_employeeID.name)])
                for info in employeeInfo:
                    vals = {
                        'kb_employeeID': rec.kb_employeeID.name,
                        'kb_reasonID': rec.kb_reasonID.kb_reason,
                        'kb_date': rec.kb_date,
                        'kb_responsible': rec.kb_responsible.name,
                        'kb_branchID': info.kb_branchID.name,
                        'kb_branchName': rec.kb_branchName.name,
                        'kb_country_id': info.country_id.name,
                        'kb_job_title': info.job_title,
                        'to_branch': rec.to_branch.name,
                        'nationality_name':info.nationality_name,
                        'weekday_label':rec.weekday_label,
                    }
                    employeeTransfer_list.append(vals)
                return self.env.ref('kb_hr_tahtheeb.employee_transfer_reportID').report_action(self, data=data)
            # Call Report 4 'تثبيت الراتب'
            elif self.kb_reportType == 'report4':
                assignment_list = []
                salary_ids_list = []

                # Searching for employee information
                employeeInfo = self.env['hr.employee'].search([('id', '=', self.kb_employeeID.id)])

                for info in employeeInfo:
                    vals = {
                        'kb_employeeID': self.kb_employeeID.name,  # Replace rec with self
                        'kb_reasonID': self.kb_reasonID.kb_reason,  # Replace rec with self
                        'kb_responsible': self.kb_responsible.name,  # Replace rec with self
                        'kb_date': self.kb_date.strftime('%d-%m-%Y'),  # Replace rec with self
                        'kb_date_to': self.kb_date_to,  # Replace rec with self
                        'kb_branchName': self.kb_branchName.name,  # Replace rec with self
                        'kb_branchNamesecond': self.kb_branchNamesecond.name,  # Replace rec with self
                        'kb_teacher_job_description': info.kb_teacher_job_description,
                        'kb_branchID': info.kb_branchID.name,
                        'kb_country_id': info.country_id.name,
                        'nationality_name':info.nationality_name,
                        'kb_job_title': info.job_title,
                        'identification_id': info.identification_id,
                    }
                    assignment_list.append(vals)

                    # If the employee has contracts, retrieve wage and allowance details
                    if info.contract_ids:
                        for contract in info.contract_ids:
                            salary_vals = {
                                'wage': contract.wage,
                                'travel_allowance': getattr(contract, 'travel_allowance', 0),
                                # Using getattr to avoid KeyError
                                'hra': getattr(contract, 'hra', 0),
                                # Handle if this field is also missing
                                'name': info.name,
                                'job_id': info.job_id.name,
                                'identification_id': info.identification_id,
                                'date_start':contract.date_start,
                            }
                            salary_ids_list.append(salary_vals)

                    else:
                        raise ValidationError("Employee Does Not have a Contract \n الموظف ليس لديه عقد")

                # Preparing data to pass to the report
                data = {
                    'form_data': self.read()[0],
                    'assignmentID': assignment_list,
                    'salary_list_loop': salary_ids_list,
                    'result_ids': [],
                }

                # Pass the data to the report
                return self.env.ref('kb_hr_tahtheeb.action_Fixation_salary_French_report').report_action(self,
                                                                                                         data=data)
            # Call Report 7 'شهادة خبرة'
            elif self.kb_reportType == 'report7':
                employee_ids = self.env['hr.employee'].search([('id', '=', self.kb_employeeID.id)])
                experienceCertificate_ids_list = []
                for i in employee_ids:
                    if i.contract_ids:
                        for x in i.contract_ids:
                            vals = {
                                'name': i.name,
                                'job_title': i.job_title,
                                # 'first_contract_date': i.first_contract_date,
                            }
                            experienceCertificate_ids_list.append(vals)
                    else:
                        raise ValidationError("Employee Does Not have a Contract \n الموظف ليس لديه عقد ")

                data = {
                    'form_data': self.read()[0],
                    'experienceCertificate_list_loop': experienceCertificate_ids_list,
                    'result_ids': [],
                }
                return self.env.ref('kb_hr_tahtheeb.kb_hr_experience_certificate_ids').report_action(self, data=data)
            # Call Report 8 'تعريف الراتب'
            elif self.kb_reportType == 'report8':
                assignment_list = []
                salary_ids_list = []

                # Searching for employee information
                employeeInfo = self.env['hr.employee'].search([('id', '=', self.kb_employeeID.id)])

                for info in employeeInfo:
                    vals = {
                        'kb_employeeID': self.kb_employeeID.name,  # Replace rec with self
                        'kb_reasonID': self.kb_reasonID.kb_reason,  # Replace rec with self
                        'kb_responsible': self.kb_responsible.name,  # Replace rec with self
                        'kb_date': self.kb_date.strftime('%d-%m-%Y'),  # Replace rec with self
                        'kb_date_to': self.kb_date_to,  # Replace rec with self
                        'kb_branchName': self.kb_branchName.name,  # Replace rec with self
                        'kb_branchNamesecond': self.kb_branchNamesecond.name,  # Replace rec with self
                        'kb_teacher_job_description': info.kb_teacher_job_description,
                        'kb_branchID': info.kb_branchID.name,
                        'kb_country_id': info.country_id.name,
                        'nationality_name':info.nationality_name,
                        'kb_job_title': info.job_title,
                        'identification_id': info.identification_id,
                    }
                    assignment_list.append(vals)
                    contract_id = self.env['hr.contract'].search([('employee_id','=',info.id),('state','=','open')])
                    if not contract_id:
                        raise UserError('لا يوجد عقد منتهي الصلاحية مرتبط  بالموظف')
                    # If the employee has contracts, retrieve wage and allowance details
                    if info.contract_ids:
                        for contract in info.contract_ids:
                            salary_vals = {
                                'wage': contract.wage,
                                'travel_allowance': getattr(contract, 'travel_allowance', 0),
                                # Using getattr to avoid KeyError
                                'hra': getattr(contract, 'hra', 0),
                                # Handle if this field is also missing
                                'name': info.name,
                                'job_id': info.job_id.name,
                                'identification_id': info.identification_id,
                                'date_start':contract.date_start,
                            }
                            salary_ids_list.append(salary_vals)

                    else:
                        raise ValidationError("Employee Does Not have a Contract \n الموظف ليس لديه عقد")

                # Preparing data to pass to the report
                data = {
                    'form_data': self.read()[0],
                    'assignmentID': assignment_list,
                    'salary_list_loop': salary_ids_list,
                    'result_ids': [],
                }

                # Pass the data to the report
                return self.env.ref('kb_hr_tahtheeb.defintion_of_salary_ids_wizard').report_action(self, data=data)
            # Call Report 10 'عرض وظيفي'
            elif self.kb_reportType == 'report10':
                data = {
                    'form_data': self.read()[0],
                    'employee_list': [],
                    'result_ids': [],
                }
                return self.env.ref('kb_hr_tahtheeb.employee_offer_report_action').report_action(self, data=data)
            # Call Report 11 'انهاء عقد مكتب التعليم'
            elif self.kb_reportType == 'report11':
                data = {
                    'form_data': self.read()[0],
                    'employee_list': [],
                    'result_ids': [],
                }
                for employee in self.kb_employeeID:
                    if employee:
                        domain = [('id', '=', employee.id)]
                        employee_domain = self.env['hr.employee'].search(domain)

                        for emp in employee_domain:
                            employee_list = []
                            contract_id = self.env['hr.contract'].search([('employee_id','=',emp.id),('state','=','close')])
                            if not contract_id:
                                raise UserError('لا يوجد عقد منتهي الصلاحية مرتبط  بالموظف')
                            vals = {
                                'employee_name': emp.name,
                            }
                            employee_list.append(vals)

                            data['employee_list'].append({
                                'employees': employee_list,
                                'employee_name': emp.name,
                                'weekday_label':rec.weekday_label,
                                'date_end':contract_id.date_end,
                            })
                return self.env.ref('kb_hr_tahtheeb.termination_education_office_contract').report_action(self,
                                                                                                          data=data)
            # Call Report 12 'انذار اساءة سلوك'
            elif self.kb_reportType == 'report12':
                data = {
                    'form_data': self.read()[0],
                    'employee_list': [],
                    'result_ids': [],
                }
                for employee in self.kb_employeeID:
                    if employee:
                        domain = [('id', '=', employee.id)]
                        employee_domain = self.env['hr.employee'].search(domain)
                        for emp in employee_domain:
                            employee_list = []
                            vals = {
                                'employee_name': emp.name,
                            }
                            employee_list.append(vals)

                            data['employee_list'].append({
                                'employees': employee_list,
                                'employee_name': emp.name,
                            })
                return self.env.ref('kb_hr_tahtheeb.report_misconduct_action_last').report_action(self, data=data)
            # Call Report 13 'انذار تاخير'
            elif self.kb_reportType == 'report13':
                data = {
                    'form_data': self.read()[0],
                    'employee_list': [],
                    'result_ids': [],
                }
                for employee in self.kb_employeeID:
                    if employee:
                        domain = [('id', '=', employee.id)]
                        employee_domain = self.env['hr.employee'].search(domain)
                        for emp in employee_domain:
                            employee_list = []
                            vals = {
                                'employee_name': emp.name,
                            }
                            employee_list.append(vals)

                            data['employee_list'].append({
                                'employees': employee_list,
                                'employee_name': emp.name,
                                'kb_date_to': rec.kb_date_to,
                            })
                return self.env.ref('kb_hr_tahtheeb.kb_regarding_delay').report_action(self, data=data)
            # Call Report 14 'بيانات وظيفية لعقد'
            elif self.kb_reportType == 'report14':
                assignment_list = []
                salary_ids_list = []

                # Searching for employee information
                employeeInfo = self.env['hr.employee'].search([('id', '=', self.kb_employeeID.id)])

                for info in employeeInfo:
                    vals = {
                        'kb_employeeID': self.kb_employeeID.name,  # Replace rec with self
                        'kb_reasonID': self.kb_reasonID.kb_reason,  # Replace rec with self
                        'kb_responsible': self.kb_responsible.name,  # Replace rec with self
                        'kb_date': self.kb_date.strftime('%d-%m-%Y'),  # Replace rec with self
                        'kb_date_to': self.kb_date_to,  # Replace rec with self
                        'kb_branchName': self.kb_branchName.name,  # Replace rec with self
                        'kb_branchNamesecond': self.kb_branchNamesecond.name,  # Replace rec with self
                        'kb_teacher_job_description': info.kb_teacher_job_description,
                        'kb_branchID': info.kb_branchID.name,
                        'kb_country_id': info.country_id.name,
                        'kb_job_title': info.job_title,
                        'identification_id': info.identification_id,
                        'certificate': info.certificate,
                        'nationality_name':info.nationality_name,
                        'experiance':info.experiance,

                    }
                    assignment_list.append(vals)

                    # If the employee has contracts, retrieve wage and allowance details
                    if info.contract_ids:
                        for contract in info.contract_ids:
                            salary_vals = {
                                'wage': contract.wage,
                                'travel_allowance': getattr(contract, 'travel_allowance', 0),
                                # Using getattr to avoid KeyError
                                'hra': getattr(contract, 'hra', 0),
                                # Handle if this field is also missing
                                'name': info.name,
                                'job_id': info.job_id.name,
                                'identification_id': info.identification_id,
                            }
                            salary_ids_list.append(salary_vals)

                    else:
                        raise ValidationError("Employee Does Not have a Contract \n الموظف ليس لديه عقد")

                # Preparing data to pass to the report
                data = {
                    'form_data': self.read()[0],
                    'assignmentID': assignment_list,
                    'salary_list_loop': salary_ids_list,
                    'result_ids': [],
                }

                # Pass the data to the report
                return self.env.ref('kb_hr_tahtheeb.job_data_for_contract_action').report_action(self, data=data)
            # Call Report 15 'تعديل راتب مسمى وظيفي'
            elif self.kb_reportType == 'report15':
                data = {
                    'form_data': self.read()[0],
                    'employee_list': [],
                    'result_ids': [],
                }
                for employee in self.kb_employeeID:
                    if employee:
                        domain = [('id', '=', employee.id)]
                        employee_domain = self.env['hr.employee'].search(domain)
                        for emp in employee_domain:
                            employee_list = []
                            vals = {
                                'employee_name': emp.name,
                            }
                            employee_list.append(vals)

                            data['employee_list'].append({
                                'employees': employee_list,
                                'employee_name': emp.name,
                            })
                return self.env.ref('kb_hr_tahtheeb.salary_adjustment_job_title_action').report_action(self, data=data)
            # Call Report 16 'خطاب تمديد'
            elif self.kb_reportType == 'report16':
                data = {
                    'form_data': self.read()[0],
                    'employee_list': [],
                    'result_ids': [],
                }
                for employee in self.kb_employeeID:
                    if employee:
                        domain = [('id', '=', employee.id)]
                        employee_domain = self.env['hr.employee'].search(domain)
                        for emp in employee_domain:
                            employee_list = []
                            vals = {
                                'employee_name': emp.name,
                            }
                            employee_list.append(vals)

                            data['employee_list'].append({
                                'employees': employee_list,
                                'employee_name': emp.name,
                                'gender':emp.gender,
                            })
                return self.env.ref('kb_hr_tahtheeb.kb_extension_letter_action').report_action(self, data=data)
            # Call Report 17 'نموذج انهاء عقد 2024'
            elif self.kb_reportType == 'report17':
                data = {
                    'form_data': self.read()[0],
                    'employee_list': [],
                    'result_ids': [],
                }
                for employee in self.kb_employeeID:
                    if employee:
                        domain = [('id', '=', employee.id)]
                        employee_domain = self.env['hr.employee'].search(domain)
                        for emp in employee_domain:
                            employee_list = []
                            vals = {
                                'employee_name': emp.name,
                            }
                            employee_list.append(vals)

                            data['employee_list'].append({
                                'employees': employee_list,
                                'employee_name': emp.name,
                                'job_id': emp.job_id.name,
                                'kb_branchName': rec.kb_branchName.name,

                            })
                return self.env.ref('kb_hr_tahtheeb.contract_termination_form_2024_action').report_action(self,
                                                                                                          data=data)
            # Call Report 18  'نموذج بيان الرغبة بالاستمرارية -1 2024 معتمد'
            elif self.kb_reportType == 'report18':
                data = {
                    'form_data': self.read()[0],
                    'employee_list': [],
                    'result_ids': [],
                }
                for employee in self.kb_employeeID:
                    if employee:
                        domain = [('id', '=', employee.id)]
                        employee_domain = self.env['hr.employee'].search(domain)
                        for emp in employee_domain:
                            employee_list = []
                            vals = {
                                'employee_name': emp.name,
                                'job_id': emp.job_id,
                            }
                            employee_list.append(vals)

                            data['employee_list'].append({
                                'employees': employee_list,
                                'employee_name': emp.name,
                                'job_id': emp.job_id.name,
                                'kb_branchName': rec.kb_branchName.name,
                            })
                return self.env.ref('kb_hr_tahtheeb.continuity_desire_statement_action').report_action(self, data=data)
            # Call Report 19  'إبراء ذمة'
            elif self.kb_reportType == 'report19':
                date_now = fields.datetime.now()
                
                data = {
                    'form_data': self.read()[0],
                    'employee_list': [],
                    'result_ids': [],
                    'hijri_date_now':self.convert_to_hijri(date_now),
                }
                for employee in self.kb_employeeID:
                    if employee:
                        domain = [('id', '=', employee.id)]
                        employee_domain = self.env['hr.employee'].search(domain)
                        for emp in employee_domain:
                            contract_id = self.env['hr.contract'].search([('employee_id','=',emp.id),('state','=','close')])
                            if not contract_id:
                                raise UserError('لا يوجد عقد منتهي الصلاحية مرتبط  بالموظف')
                            employee_list = []
                            vals = {
                                'employee_name': emp.name,
                                'job_id': emp.job_id,
                                'identification_id': emp.identification_id,
                                
                            }
                            employee_list.append(vals)

                            data['employee_list'].append({
                                'employees': employee_list,
                                'employee_name': emp.name,
                                'job_id': emp.job_id.name,
                                'gender':emp.gender,
                                'nationality_name':emp.nationality_name,
                                'from_date':contract_id.date_start,
                                'from_date_h':self.convert_to_hijri(contract_id.date_start),
                                'to_date':contract_id.date_end,
                                'to_date_h':self.convert_to_hijri(contract_id.date_end),
                                'kb_country_id': emp.country_id.name,
                                'identification_id': emp.identification_id,

                            })
                return self.env.ref('kb_hr_tahtheeb.action_receivables_report').report_action(self, data=data)
            # Call Report 20  'إتفاقية سرية المعلومات'
            elif self.kb_reportType == 'report20':
                data = {
                    'form_data': self.read()[0],
                    'employee_list': [],
                    'result_ids': [],
                }
                for employee in self.kb_employeeID:
                    if employee:
                        domain = [('id', '=', employee.id)]
                        employee_domain = self.env['hr.employee'].search(domain)
                        for emp in employee_domain:
                            employee_list = []
                            vals = {
                                'employee_name': emp.name,
                                'job_id': emp.job_id,
                            }
                            employee_list.append(vals)

                            data['employee_list'].append({
                                'employees': employee_list,
                                'employee_name': emp.name,
                                'job_id': emp.job_id.name,
                                'kb_country_id': emp.country_id.name,
                                'nationality_name':emp.nationality_name,
                                'identification_id': emp.identification_id,
                                'weekday_label':rec.weekday_label,

                            })
                return self.env.ref('kb_hr_tahtheeb.confidentiality_agreement_action').report_action(self, data=data)
            # Call Report 21  'شهادة خبره واخلاء طرف'
            elif self.kb_reportType == 'report21':
                assignment_list = []
                data = {
                    'form_data': self.read()[0],
                    'assignmentID': assignment_list
                }
                employeeInfo = self.env['hr.employee'].search([('id', '=', self.kb_employeeID.id)])

                for info in employeeInfo:
                    contract_id = self.env['hr.contract'].search([('employee_id','=',info.id),('state','=','open')])
                    if not contract_id:
                        raise UserError('لا يوجد عقد منتهي الصلاحية مرتبط  بالموظف')
                    vals = {
                        'kb_employeeID': rec.kb_employeeID.name,
                        'kb_reasonID': rec.kb_reasonID.kb_reason,
                        'kb_responsible': rec.kb_responsible.name,
                        'kb_date': contract_id.date_start,
                        'kb_date_to': contract_id.date_end,
                        'kb_branchName': rec.kb_branchName.name,
                        'kb_branchNamesecond': rec.kb_branchNamesecond.name,
                        'kb_teacher_job_description': info.kb_teacher_job_description,
                        'kb_branchID': info.kb_branchID.name,
                        'kb_country_id': info.country_id.name,
                        'kb_job_title': info.job_title,
                        'kb_nationality': info.nationality_name,
                        'identification_id': info.identification_id,


                    }
                    assignment_list.append(vals)
                return self.env.ref('kb_hr_tahtheeb.certificate_experience_clearance_action').report_action(self,
                                                                                                            data=data)
            # Call Report 22  'عرض وظيفي - اداري'
            elif self.kb_reportType == 'report22':
                assignment_list = []
                salary_ids_list = []

                # Searching for employee information
                employeeInfo = self.env['hr.employee'].search([('id', '=', self.kb_employeeID.id)])

                for info in employeeInfo:
                    vals = {
                        'kb_employeeID': self.kb_employeeID.name,  # Replace rec with self
                        'kb_reasonID': self.kb_reasonID.kb_reason,  # Replace rec with self
                        'kb_responsible': self.kb_responsible.name,  # Replace rec with self
                        'kb_date': self.kb_date.strftime('%d-%m-%Y'),  # Replace rec with self
                        'kb_date_to': self.kb_date_to,  # Replace rec with self
                        'kb_branchName': self.kb_branchName.name,  # Replace rec with self
                        'kb_branchNamesecond': self.kb_branchNamesecond.name,  # Replace rec with self
                        'kb_teacher_job_description': info.kb_teacher_job_description,
                        'kb_branchID': info.kb_branchID.name,
                        'kb_country_id': info.country_id.name,
                        'kb_job_title': info.job_title,
                        'identification_id': info.identification_id,
                        'weekday_label':self.check_the_day_name(),
                    }
                    assignment_list.append(vals)

                    # If the employee has contracts, retrieve wage and allowance details
                    if info.contract_ids:
                        for contract in info.contract_ids:
                            salary_vals = {
                                'wage': contract.wage,
                                'travel_allowance': getattr(contract, 'travel_allowance', 0),
                                # Using getattr to avoid KeyError
                                'hra': getattr(contract, 'hra', 0),
                                # Handle if this field is also missing
                                'name': info.name,
                                'job_id': info.job_id.name,
                                'identification_id': info.identification_id,
                            }
                            salary_ids_list.append(salary_vals)

                    else:
                        raise ValidationError("Employee Does Not have a Contract \n الموظف ليس لديه عقد")

                # Preparing data to pass to the report
                data = {
                    'form_data': self.read()[0],
                    'assignmentID': assignment_list,
                    'salary_list_loop': salary_ids_list,
                    'result_ids': [],
                }

                return self.env.ref('kb_hr_tahtheeb.administrative_new_job_offer_action').report_action(self, data=data)
            # Call Report 23  'نموذج ساعات اضافية - مدارس'
            elif self.kb_reportType == 'report23':
                data = {
                    'form_data': self.read()[0],
                    'employee_list': [],
                    'result_ids': [],
                }
                for employee in self.kb_employeeID:
                    if employee:
                        domain = [('id', '=', employee.id)]
                        employee_domain = self.env['hr.employee'].search(domain)
                        for emp in employee_domain:
                            employee_list = []
                            vals = {
                                'employee_name': emp.name,
                                'job_id': emp.job_id,
                            }
                            employee_list.append(vals)

                            data['employee_list'].append({
                                'employees': employee_list,
                                'employee_name': emp.name,
                                'job_id': emp.job_id.name,
                                'kb_branchName': rec.kb_branchName.name,
                                'kb_date': rec.kb_date.strftime('%d-%m-%Y'),
                                'kb_date_to': rec.kb_date_to,
                            })
                return self.env.ref('kb_hr_tahtheeb.additional_hours_schools_action').report_action(self, data=data)
            # Call Report 24  'نموذج ساعات اضافية - ادارة'
            elif self.kb_reportType == 'report24':
                data = {
                    'form_data': self.read()[0],
                    'employee_list': [],
                    'result_ids': [],
                }
                for employee in self.kb_employeeID:
                    if employee:
                        domain = [('id', '=', employee.id)]
                        employee_domain = self.env['hr.employee'].search(domain)
                        for emp in employee_domain:
                            employee_list = []
                            vals = {
                                'employee_name': emp.name,
                                'job_id': emp.job_id,
                            }
                            employee_list.append(vals)

                            data['employee_list'].append({
                                'employees': employee_list,
                                'employee_name': emp.name,
                                'job_id': emp.job_id.name,
                                'kb_branchName': rec.kb_branchName.name,
                                'kb_date': rec.kb_date.strftime('%d-%m-%Y'),
                                'kb_date_to': rec.kb_date_to,
                            })
                return self.env.ref('kb_hr_tahtheeb.additional_hours_department_action').report_action(self, data=data)
