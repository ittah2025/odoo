from datetime import date
from odoo import api, fields, models,_
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class transport_registration(models.Model):
    _name = 'transport_registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Registration Transport'
    _rec_name = 'student_id'


    student_id = fields.Many2one("student", "Student Name", help="Select Student")
    transportRoot = fields.Many2one('tran_information', 'Transport Root Name ')
    RegistrationForMonths = fields.Integer(string="Registration For Months")
    PaidAmount = fields.Float(string="Monthly Amount", related="transportRoot.KB_price")
    reg_date = fields.Date(
        "Registration Date",
        readonly=True,
        help="Start Date of registration",
        default=fields.Date.context_today,
    )
    reg_end_date = fields.Date(
        "Registration End Date",
        readonly=True,
        help="Start Date of registration",
        compute='onchange_registration_month'
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('send', 'Send'),
        ('reject', 'Reject'),
        ('topaid', 'Accept and To Paid'),
        ('registration', 'Registered'),
        ('done', 'Done'),
    ], string='Status', default='draft', readonly=True)

    fees_ids=fields.Many2one('fees')

    @api.onchange("RegistrationForMonths")
    def onchange_registration_month(self):
        """Method to compute registration end date."""
        tr_start_date = fields.Date.today()
        tr_end_date = tr_start_date + relativedelta(
            months=self.RegistrationForMonths)
        self.reg_end_date = tr_end_date

    def send_state(self):
        self.state = 'send'

    def topaid_state(self):
        self.state = 'topaid'
        for record in self:
            fees_ids=self.env['fees'].create({
                                    'student_id': record.student_id.id,
                                    'date':record.reg_date,
                                    'structure_id':3,
                                    'payment_type':"month",
                                    'paymentNumber':record.RegistrationForMonths,
                                    'fees_line_ids': [(0, 0, {
                                        'amount':record.PaidAmount * record.RegistrationForMonths,
                                        'name':'الرسوم النقل/ Transportation fees',
                                    })],
                                })
            record.fees_ids=fees_ids

    def reject_state(self):
        self.state = 'reject'

    def registration_state(self):
        for rec in self:
            for record in rec.fees_ids:
                for paid in record.payments_line_ids:
                    if paid.isPaid:
                        self.state = 'registration'

    def done_state(self):
        today = date.today()
        for rec in self:
            if rec.reg_end_date <= today:
                self.state = 'done'
