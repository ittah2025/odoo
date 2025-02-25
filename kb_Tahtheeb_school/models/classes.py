from email.policy import default
#from typing_extensions import Required
from odoo import api, fields, models,_
from datetime import date
import re
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime,timedelta

class classes(models.Model):
    _name = "classes"
    _table = "classes"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "class form"
    _rec_name = 'combination'


    student_id = fields.Many2one('student', string="Student")
    numbers_of_student=fields.Integer(string="Student numbers")
    check_limit_number=fields.Boolean (string="Is limit student?",default=True)
    class_id = fields.Char(string='Class ID', required=True,
                            copy=False, readonly=True, default=lambda self: ('New'))
    name = fields.Char(string='Name', required=True, translate=True, help='Enter the class name')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], readonly=True, default="draft", help='Choose the class state')
    
    studentID = fields.Many2many('student', string="Students", required=True)
    school_id = fields.Many2one('school', string='School', help='choose school', required=False)
    study_year = fields.Many2one('academic_year', string="Academic Year", required=False)
    grad_id=fields.Many2one('grade', string='Grade', help='choose grade', required=False)
    note = fields.Char()

    teacher_tabel_ids = fields.One2many('teacher_tabel_line', 'teacher_tabel_id', string='teacher tabel line')
    # teacher_tabel=fields.Many2one('teacher_tabel_line')
    combination = fields.Char(string='Combination', compute='_compute_fields_combination')

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Student'
        if vals.get('class_id', ('New')) == ('New'):
            vals['class_id'] = self.env['ir.sequence'].next_by_code('classes') or ('New')
        res = super(classes, self).create(vals)
        return res

        # if acdimec year done will chang

    deflt = fields.Boolean(string=' ', default=True)

    def action_Done(self):
        current = self.env['academic_year'].search([('current', '=', self.deflt)])
        for rec in self:
            for record in current:
                dateclass = rec.Date_class.strftime("%d/%m/%Y %H:%M:%S")
                if str(dateclass) < str(record.date_stop):
                    rec.state = 'done'
                else:
                    raise ValidationError('The Academic year not end yet')

    def action_confirm(self):
        for rec in self:
            for record in rec.teacher_tabel_ids:
               self.env['teachertable'].create({
                    'teacher_id': record.teacher_id.id,
                    'subject_id': record.subject_id.id,
                    'class_id': rec.id,
                    'class_duration': record.class_duration,
                    'Date_class': record.Date_class,
                   'state':'confirm'
                })
               self.env['kb_student_table'].create({
                    'teacher_id': record.teacher_id.id,
                    'subject_id': record.subject_id.id,
                    'class_id': rec.id,
                    'class_duration': record.class_duration,
                    'Date_class': record.Date_class,
                   'state':'confirm'
                })
            rec.state = 'confirm'

    @api.depends('name', 'grad_id')
    def _compute_fields_combination(self):
        for test in self:
            test.combination = test.name + ' ' + '-' + ' ' + str(test.grad_id.name)

class teacher_tabel_line(models.Model):
    _name = "teacher_tabel_line"
    _description = "Teacher Table line "
    _inherit = ['mail.thread', 'mail.activity.mixin']

    teacher_id = fields.Many2one('teacher', string="Teacher Name", required=False,)
    subject_id = fields.Many2one('subject', string="Subject Name", required=False)
    class_duration = fields.Float(string='Class Duration', required=False)
    Date_class = fields.Datetime(string="Date Class", required=False)

    teacher_tabel_id = fields.Many2one('classes', string='teacher tabel line')

    # Room name is related to apartment
    @api.onchange('teacher_id')
    def onchange_apartment(self):
        for rec in self:
            return {'domain': {'subject_id': [('name', '=', rec.teacher_id.subject_id.name)]}}

    # @api.onchange('Date_class')
    # def check_if_have_class(self):
    #     teacher = self.env["teachertable"].search([('teacher_id', '=', self.teacher_id.id)])
    #     for record in self:
    #         for rec in teacher:
    #             test = record.Date_class + timedelta(hours=3)
    #             timeendself = test.strftime("%Y/%m/%d %H:%M:%S")
    #             test2 = rec.Date_class + timedelta(hours=3)
    #             timestartteach = test2.strftime("%Y/%m/%d %H:%M:%S")
    #             timeend = rec.Date_class + timedelta(hours=rec.class_duration + 4)
    #             timeends = timeend.strftime("%Y/%m/%d %H:%M:%S")
    #             if rec.state == 'confirm':
    #                 if record.Date_class == rec.Date_class:
    #                     if (timestartteach < timeendself) or (timeendself < timeends):
    #                         raise ValidationError(_('Teacher have class in same time'))
    #             else:
    #                 pass


