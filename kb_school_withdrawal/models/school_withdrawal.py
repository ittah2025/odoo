# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime, timedelta, date

class school_withdrawal(models.Model):
    _name = 'school_withdrawal'
    _table = 'school_withdrawal'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'mail.render.mixin']
    _rec_name = 'withdrawalID'
    name = fields.Char(string="Name")
    withdrawalID = fields.Char(string='ID', required=False,
                               copy=False, readonly=True, default=lambda self: ('New'))
    note = fields.Text(string="Description")
    kb_note = fields.Text(string="Description", tracking=1)
    kb_date = fields.Date(string="Date", tracking=1)
    student_id = fields.Many2one('student', string="Student", tracking=1)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('withdrawal_administrator', 'Approved by withdrawal administrator'),
        ('approved_education_admin_employee', 'Approved by education admin employee'),
        ('rejected_education_admin_employee', 'Rejected by education admin employee'),
        ('approved_collection_employee', 'Approved by collection employee'),
        ('rejected_collection_employee', 'Rejected by collection employee'),
        ('school_agent_done', 'Done'),
    ], readonly=True, default="draft", help='Choose the state', tracking=1)

    withdrawal_reason = fields.Selection([
        ('change_of_place', 'Change of place of residence'),
        ('fees_high', 'Fees are high'),
        ('school_building', 'The school building is not set'),
        ('educational_path', 'Change educational path'),
        ('educational_staff', 'Educational Staff'),
    ],string="reason for withdrawal", help='Choose the reason for withdrawal', tracking=1)
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New ID'
        if vals.get('withdrawalID', ('New')) == ('New'):
            vals['withdrawalID'] = self.env['ir.sequence'].next_by_code(
                'school_withdrawal') or ('New')
        res = super(school_withdrawal, self).create(vals)
        return res


    def action_withdrawal_administrator(self):
        self.state = 'withdrawal_administrator'

    def approved_education_admin_employee(self):
        self.state = 'approved_education_admin_employee'

    def rejected_education_admin_employee(self):
        self.state = 'rejected_education_admin_employee'

    def approved_collection_employee(self):
        self.state = 'approved_collection_employee'

    def rejected_collection_employee(self):
        self.state = 'rejected_collection_employee'

    def school_agent_done(self):
        self.state = 'school_agent_done'