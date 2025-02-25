from email.policy import default
#from typing_extensions import Required
from odoo import api, fields, models
from datetime import date

import re

class subject(models.Model):
    _name = "subject"
    _table = "subject"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Subjects"

    name = fields.Char(string="Name", required=True)
    subject_id = fields.Char(string='Subject ID', required=True,
                            copy=False, readonly=True, default=lambda self: ('New'))
    code= fields.Char('Code', required=True, help='Subject code')

    school_id = fields.Many2one('school', string='School', help='choose school', required=False)


    grade_id=fields.Many2many('grade','subject_ids', string='Grade',required=False)
    teacher_ids=fields.Many2many('teacher' ,string='Teachers',required=False)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], readonly=True, default="draft", help='Choose the class state')
    
    max_mark = fields.Integer(string="Maximum marks", required=True)
    min_mark = fields.Integer(string="Minimum marks", required=True)
    
    note = fields.Char()

    Hours=fields.Float(string="Credit Hours", required=False)
    Grade_points=fields.Float(string="Grade Points", required=False)
    elective_id = fields.Many2one('elective_subject',
                                  help='''Elective subject respective
                                     the following subject''')

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New subject'

        if vals.get('subject_id', ('New')) == ('New'):
            vals['subject_id'] = self.env['ir.sequence'].next_by_code(
                'subject') or ('New')
        res = super(subject, self).create(vals)
        return res

    amount = fields.Float()


class elective_subject(models.Model):
    _name = "elective_subject"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Elective Subject"

    name = fields.Char(string="Name", required=True)
    grade_id = fields.Many2one('grade', string='Grade', required=False)

    subject_ids = fields.One2many('subject', 'elective_id','Elective Subjects', help='''Subjects of the respective elective subject''')
    elective_subject_ids = fields.Many2many('subject',
                                            'elective_subject_rel',
                                            'elective_id',
                                            'subject_id',
                                            'Elective Subjects',
                                            help='''Subjects of the
                                                respective elective subject''')
