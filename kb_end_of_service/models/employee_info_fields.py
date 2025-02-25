from odoo import api, fields, models, _
from logging import getLogger
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime, timedelta
_logger = logging.getLogger(__name__)

class employee_info_fields(models.Model):

    _inherit = 'hr.employee'

    tday = datetime.today()
    contract_end_date      = fields.Date   (string="Contract End date", default =tday                                       )
    total_years            = fields.Integer(string="Years"            , compute ="get_total_Years"                          )
    total_salary           = fields.Float  (string="Total wage"       , readonly=True, compute="get_employee_info"          )
    total_daily_rates      = fields.Float  (string="Total Daily Rate" , readonly=True, compute="get_employee_dailyrates"    )
    remaining_days         = fields.Integer(string="Remaining Days"   , readonly=True, compute="get_employee_remaining_days")
    total_remaining_salary = fields.Float  (string="Remaining Salary" , readonly=True, compute="get_remaining_salary"       )
    total_reward_remaining = fields.Float  (string="Total Reward"     , readonly=True, compute="total_all"       )
    total_loan             = fields.Float  (string="Total Loans"      , readonly=True, compute="get_total_loans"            )
    clicked = fields.Boolean(string="")
    
    
    

    time_off_remaining_id = fields.Float(string="Remaining time off"       , readonly=True, compute="action_leave_time"   )
    time_off_salary_id    = fields.Float(string="Remaining salary time off", readonly=True, compute="total_time")

    type_contract = fields.Selection([
        ('specific', 'specified contract time '),
        ('notspecific', 'None specified contract time'),
        ], string='Type of contract', default='specific')

    # joining_date
    # contract_id
    # contract_id.wage
    # leaves_count
    @api.onchange('contract_end_date')
    def action_leave_time(self):

        employee_ids = self.env['hr.leave'].search([('employee_ids', '=', self.id)])

        i = 0.0
        i = float(self.allocation_display)
        ii = 0.0
        ii = float(self.allocation_remaining_display)
        time_off_remaining = self.allocation_remaining_display

        self.time_off_remaining_id = time_off_remaining




        # print(self.allocation_display)
        # print(self.allocation_remaining_display)


    @api.depends('contract_end_date')
    def get_employee_info(self):
        total_wage = self.contract_id.wage + self.contract_id.hra + self.contract_id.da + self.contract_id.travel_allowance + self.contract_id.meal_allowance + self.contract_id.medical_allowance + float(self.contract_id.other_allowance) 
        self.total_salary = total_wage
        # date_id = self.env['hr.contract'].search([('employee_id', '=', self.id)])
        # print(total_wage)

    @api.depends('contract_end_date')
    def get_total_loans(self):
        loans_id = self.env['hr.loan'].search([('employee_id', '=', self.id),('state','=','approve')])
        if loans_id:
            for loans_ids in loans_id:
                self.total_loan  +=  loans_ids.balance_amount
        else:
            self.total_loan = 0


    @api.onchange('contract_end_date')
    def get_employee_dailyrates(self):
        daily_rates = self.total_salary /30
        self.total_daily_rates = daily_rates

    @api.onchange('contract_end_date')
    def get_employee_remaining_days(self):
        if self.contract_end_date:
            day_count = self.contract_end_date.strftime("%d")
            # print(self.contract_end_date)
            self.remaining_days = day_count
        else:
            self.remaining_days = 0


    @api.onchange('contract_end_date')
    def get_remaining_salary(self):
        remaining_salary = (self.total_daily_rates * self.remaining_days) + self.Reward
        self.total_remaining_salary = remaining_salary





# Calculate number of total work days
    total_days = fields.Integer(string="Days", compute="get_total_days")
    @api.depends('contract_end_date')
    def get_total_days(self):
        for rec in self:
            if rec.joining_date and rec.contract_end_date:
                totalper = rec.contract_end_date - rec.joining_date
                totalfinal = totalper.days
                rec.total_days = totalfinal
            else:
                rec.total_days = 0


    specific = fields.Selection([
        ('reason1', 'The expiration of the contract period or the agreement of the two parties to terminate the contract '),
        ('reason2', 'Termination of the contract by the employer'),
        ('reason3', 'Termination of the contract by the employer for one of the cases mentioned in Article 80 '),
        ('reason4', 'Leaving work as a result of force majeure '),
        ('reason5', 'The worker termination of the work contract within six months of the marriage contract or within six months of giving birth'),
        ('reason6', 'The worker leaving work for one of the cases mentioned in Article 81'),
        ('reason7', 'Termination of the contract by the worker or the worker leaving the work in cases other than those mentioned in Article 81'),
    ], string='Reason')

    notspecific = fields.Selection([
        ('reasons1', 'The worker termination of the work contract within six months of the marriage contract or within six months of giving birth'),
        ('reasons2', 'The agreement of the worker and the employer to terminate the contract'),
        ('reasons3', 'The employees resignation'),
        ('reasons4', 'Leaving the worker to work without submitting a resignation other than the cases mentioned in Article 81'),
        ('reasons5', 'The worker left work for one of the cases mentioned in Article 81'),
        ('reasons6', 'Leaving work as a result of force majeure'),
        ('reasons7', 'Termination of the contract by the employer '),
        ('reasons8', 'Termination of the contract by the employer for one of the cases mentioned in Article 80'),
    ], string='Reason')

    covenant = fields.Selection([
        ('covenantto', 'Covenant delivered'),
        ('notcovenantto', 'Delivery has not been done'),
    ], string='covenant')



    button_set_evacuation = fields.Boolean(       'Hand over all the covenant to the worker'                             )
    button_set_covenant   = fields.Boolean(       'The act of evading a party for the worker '                           )
    RewardNotSpecific     = fields.Char   (string="Service reward"                                                       )
    RewardSpecific        = fields.Char   (string="Service reward"                                                       )
    salary                = fields.Integer(string=" salary"                                                              )
    total_month           = fields.Integer(string="Month"                                     , compute="get_total_month")
    Reward                = fields.Integer(string="Reward"                                    , compute='total_Reward'   )

    @api.depends('contract_end_date')
    def get_total_Years(self):
        for rec in self:
            if rec.joining_date and rec.contract_end_date:
                totalper = rec.contract_end_date - rec.joining_date
                totalperfinal = totalper.days
                totalfinal = totalperfinal / 365
                rec.total_years = totalfinal

            else:
                rec.total_years = 0

    @api.depends('contract_end_date')
    def get_total_month(self):
        for rec in self:
            if rec.joining_date and rec.contract_end_date:
                totalper = rec.contract_end_date - rec.joining_date
                totalperfinal = totalper.days
                totalfinal = totalperfinal / 12
                rec.total_month = totalfinal

            else:
                rec.total_month = 0

    @api.onchange('notspecific')
    def function_get_RewardNotSpecifics(self):
        for rec in self:
            if rec.notspecific == 'reasons1':
                rec.RewardNotSpecific = "From the first year to the fifth year, half the salary, after the first five years, the salary for each year"
            elif rec.notspecific == 'reasons2':
                rec.RewardNotSpecific = "From the first year to the fifth year, half the salary, after the first five years, the salary for each year"
            elif rec.notspecific == 'reasons3':
                rec.RewardNotSpecific = "From the second year to the fifth year, one-third of the bonus after the first five years, and a salary for each year "
            elif rec.notspecific == 'reasons4':
                rec.RewardNotSpecific = "Not worth a reward"
            elif rec.notspecific == 'reasons5':
                rec.RewardNotSpecific = "Reserve all rights"
            elif rec.notspecific == 'reasons6':
                rec.RewardNotSpecific = "Reserve all rights"
            elif rec.notspecific == 'reasons7':
                rec.RewardNotSpecific = "From the first year to the fifth year, half the salary, after the first five years, the salary for each year"
            elif rec.notspecific == 'reasons8':
                rec.RewardNotSpecific = "Not worth a reward "

    @api.onchange('specific')
    def function_get_RewardSpecifics(self):
        for rec in self:
            if rec.specific == 'reason1':
                rec.RewardSpecific = "From the first year to the fifth year, half the salary, after the first five years, the salary for each year"
            elif rec.specific == 'reason2':
                rec.RewardSpecific = "From the first year to the fifth year, half the salary, after the first five years, the salary for each year"
            elif rec.specific == 'reason3':
                rec.RewardSpecific = "Not worth a reward"
            elif rec.specific == 'reason4':
                rec.RewardSpecific = "Reserve all rights"
            elif rec.specific == 'reason5':
                rec.RewardSpecific = "From the first year to the fifth year, half the salary, after the first five years, the salary for each year"
            elif rec.specific == 'reason6':
                rec.RewardSpecific = "Reserve all rights"
            elif rec.specific == 'reason7':
                rec.RewardSpecific = "Not worth a reward"

    @api.onchange('total_salary')
    def total_Reward(self):
        for rec in self:
            if rec.specific == 'reason3' or rec.specific == 'reason7' or rec.notspecific == 'reasons4' or rec.notspecific == 'reasons8':
                rec.Reward = 0
            elif rec.notspecific == 'reasons3':
                if rec.total_years == 1:
                    rec.Reward = 0
                elif rec.total_years < 5:
                    stepsalary = rec.total_salary * 0.333
                    rec.Reward = (stepsalary * rec.total_years)
                else:
                    rec.Reward = (rec.total_salary * rec.total_years)
            else:
                if rec.total_years < 5:
                    stepsalary = rec.total_salary / 2
                    rec.Reward = (stepsalary * rec.total_years)
                else:
                    rec.Reward = (rec.total_salary * rec.total_years)

    @api.onchange('contract_end_date')
    def total_time(self):
        time_off_salary = self.total_daily_rates * self.time_off_remaining_id
        self.time_off_salary_id = time_off_salary

        # print(self.time_off_salary_id)

    @api.onchange('contract_end_date')
    def total_all(self):

        reward_remaining_salary = (self.total_remaining_salary + self.time_off_salary_id) - self.total_loan
        self.total_reward_remaining = reward_remaining_salary

        # print(rec.total_remaining_salary)
        # print(rec.Reward)
        # print(rec.total_loan)


    # @api.onchange('contract_end_date')
    # def get_reward_remaining(self):
    #     for rec in self:
    #         reward_remaining_salary = rec.total_remaining_salary + rec.Reward - rec.total_loan
    #         rec.total_reward_remaining = reward_remaining_salary
    #
    #         print(rec.total_remaining_salary)
    #         print(rec.Reward)
    #         print(rec.total_loan)
    #
    #         time_off_salary = rec.total_daily_rates * rec.time_off_remaining_id
    #         rec.time_off_salary_id = time_off_salary

    date_today = fields.Date(default=datetime.today())
    
    kb_journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        domain="[('type', '=', 'general'), ('company_id', '=', company_id)]")
    
    kb_timeoff_debit_account = fields.Many2one('account.account', string="Timeoff Debit Account")
    kb_salary_debit = fields.Many2one('account.account', string="Salary Debit Account")
    kb_salary_credit = fields.Many2one('account.account', string="Salary Credit Account")
    
    
    def send_journal_entries(self):
        name = str(self.name)
        a = "قيمة تصفية بدل اجازات الفترة من"
        b = str(self.date_today)
        c = "الى"
        d = str(self.joining_date)
        e = self.name

        f = a + " " + b + " " + c + " " + d + " " + e

        
        debit_vals_timeoff = {
            'name': f,
            'debit': self.time_off_salary_id,
            'credit': 0.0,
            'account_id': self.kb_timeoff_debit_account.id, #28052
            'tax_line_id': False,
        }


        debit_vals = {
            'name': f,
            'debit': self.total_remaining_salary,
            'credit': 0.0,
            'account_id': self.kb_salary_debit.id,
            'tax_line_id': False,
        }
        credit_vals = {
            'name': f,
            'debit': 0.0,
            'credit': self.total_reward_remaining,
            'account_id': self.kb_salary_credit.id,
            'tax_line_id': False,
        }
        vals = {
            'journal_id': self.kb_journal_id.id,
            'date': self.date_today,
            'state': 'draft',
            'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals), (0, 0, debit_vals_timeoff)]
        }

        move_ids = self.env['account.move'].create(vals)
        if move_ids:
            self.clicked = True
        else:
            self.clicked = False
        # return {
        #     'name': _('P'),
        #     'view_mode': 'form',
        #     'view_id': False,
        #     'view_type': 'form',
        #     'res_model': 'account.move',
        #     'res_id': move_ids.id,
        #     'type': 'ir.actions.act_window',
        #     'target': 'self',
        # }