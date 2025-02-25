# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import UserError, ValidationError


class StaffRequitment(models.Model):
    _name = 'staff.recruitment'
    _description = "Employee recruitment"
    _inherit = ['mail.thread']
    _rec_name = "sequence"

    applicant_id = fields.Many2one('res.users', string="Applicant", required=True)
    department_id = fields.Many2one('hr.department', string="Department", required=True)
    exper_start_date = fields.Date('Start Date')
    exper_end_date = fields.Date('End Date')
    experience_year = fields.Float("Years", compute='compute_years')
    job_id = fields.Many2one('hr.job', string="Job", required=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('approve', 'Approved'), ('confirm', 'Confirmed'), ('cancel', 'Cancel')], string='State',
        default='draft')
    count = fields.Integer(string="Count", compute='applicant_count')
    sequence = fields.Char(string="Order #", default=lambda self: _('New'))

    kb_Email = fields.Char("Email")
    module_a_id = fields.Many2one('module.a.model', string='Module A')
    kb_Email_CC = fields.Char("Email cc")
    kb_phone = fields.Integer("Phone")
    kb_Mobile = fields.Integer("Mobile")
    kb_Degree = fields.Float("Degree")
    kb_Expected_salary = fields.Float("Expected Salary")
    kb_Proposed_salary = fields.Float("Proposed Salary")
    kb_Availability = fields.Date("Availability")

    def action_confirm(self):
        res_obj = self.env['hr.applicant'].sudo()
        res_obj.create({
                'job_id': self.job_id.id,
                'name': self.job_id.name + '/' + self.sequence,
                'email_from':self.kb_Email,
                'email_cc':self.kb_Email_CC,
                'partner_phone':self.kb_phone,
                'partner_mobile':self.kb_Mobile,
                'salary_expected':self.kb_Expected_salary,
                'salary_proposed':self.kb_Proposed_salary,
                'availability':self.kb_Availability,
                'partner_name':self.applicant_id.name
                }
        )
        self.write({'state': 'confirm'})
        return

    def compute_years(self):
        self.experience_year = 0.0
        if self.exper_start_date and self.exper_end_date:
            new_date = self.exper_start_date
            old_date = self.exper_end_date
            delta = old_date - new_date
            self.update({'experience_year': (delta.days) / 365})

    def action_approve(self):
        self.write({'state': 'approve'})
        return

    def action_cancel(self):
        self.write({'state': 'cancel'})
        return

    def action_draft(self):
        self.write({'state': 'draft'})
        return

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            seq = self.env['ir.sequence'].next_by_code('staff.recruitment') or '/'
            vals['sequence'] = seq
        return super(StaffRequitment, self).create(vals)
    #
    def action_application(self):
        self.ensure_one()
        return {
            'name': 'Applicants',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hr.applicant',
            'domain': [('name', '=', self.job_id.name + '/' + self.sequence)],
        }

    def applicant_count(self):
        for recuitment in self:
            recuitment.count = 0
            if recuitment.state == 'confirm':
                recuitment.update({'count': self.env['hr.applicant'].search_count(
                    [('name', '=', self.job_id.name + '/' + self.sequence)])})
