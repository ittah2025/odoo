from odoo import api, fields, models
from num2words import num2words


class EmployeeOffer(models.Model):
    _name = "employee.offer.report"

    kb_date = fields.Date(default=fields.Date.today(), store=True, string='Date')
    kb_employee_name = fields.Char(string='Employee Name')
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
    kb_basic_salary_in_words = fields.Char(string='basic salary in words', compute='_compute_salary_words_2',
                                           store=True)
    location = fields.Char()
    holidays = fields.Integer()
    days_of_work = fields.Integer()
    insurance = fields.Char()
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
                # Use the language parameter to specify the desired language (e.g., 'en' for English)
                record.kb_basic_salary_in_words = num2words(record.kb_basic_salary_2, lang='ar_001')
            else:
                record.kb_basic_salary_in_words = False

    @api.depends('kb_salary')
    def _compute_salary_words(self):
        for record in self:
            if record.kb_salary:
                # Use the language parameter to specify the desired language (e.g., 'en' for English)
                record.kb_salary_words = num2words(record.kb_salary, lang='ar_001')
            else:
                record.kb_salary_words = False

    @api.depends('kb_date')
    def _compute_weekday(self):
        for record in self:
            if record.kb_date:
                weekday = fields.Date.from_string(record.kb_date).weekday()
                record.weekday = str(weekday)  # Convert to string to match the Selection values
            else:
                record.weekday = False  # or any default value you want for cases where kb_date is not set

    @api.depends('weekday')
    def _compute_weekday_label(self):
        for record in self:
            if record.weekday:
                record.weekday_label = dict(record._fields['weekday'].selection).get(record.weekday)
            else:
                record.weekday_label = False

    def action_print_report(self):
        data = {
            'form_data': self.read()[0],
            'employee_list': [],
            'result_ids': [],
        }
        return self.env.ref('kb_employee_job_offer.employee_offer_report_action').report_action(self,
                                                                                                data=data)
