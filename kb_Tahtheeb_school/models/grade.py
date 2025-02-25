from email.policy import default
#from typing_extensions import Required
from odoo import api, fields, models
from datetime import date
from odoo.exceptions import UserError, ValidationError
import re
from odoo.tools.translate import _


class grade(models.Model):
    _name = "grade"
    _table = "grade"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "grades"

    sequence=fields.Char(string="Sequence", required=True)
    code=fields.Char(string="Code", required=False)
    name = fields.Char(string="Name", required=True)
    grade_id = fields.Char(string='grade ID', required=True,
                            copy=False, readonly=True, default=lambda self: ('New'))

    school_id = fields.Many2one('school', string='School', help='choose school', required=False)
    class_id = fields.Many2many('classes', string="Class", required=False)
    student_id = fields.Many2many('student', string="student", required=False)

    subject_ids=fields.Many2one('subject', string="subject")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], readonly=True, default="draft", help='Choose the class state')

    note = fields.Char()
    
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New grade'

        if vals.get('grade_id', ('New')) == ('New'):
            vals['grade_id'] = self.env['ir.sequence'].next_by_code(
                'grade') or ('New')
        res = super(grade, self).create(vals)
        return res


    year=fields.Many2one('academic_year', string="years")

    nameyear= fields.Char(compute="show_year")
    def show_year(self):
        year=self.env['academic_year'].search([('current','=',True)])
        for record in year:
            self.nameyear = record.academic_yearID
  



class grade_line(models.Model):
    _name = 'grade_line'
    _description = 'grade line'


