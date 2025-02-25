# -*- coding: utf-8 -*-
from email.policy import default
#from typing_extensions import Required
from odoo import api, fields, models
from datetime import date
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
import re


class teacher(models.Model):
    _name = "teacher"
    _table = "teacher"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Teacher Information"
    
    photo = fields.Binary(String='photo', help='Choose the photo', required=False)
    
    teacherID = fields.Char(string='Teacher ID', required=True,
                            copy=False, readonly=True, default=lambda self: ('New'))

    teacher_nat_id = fields.Char(string="National ID", copy=False, required=True, size=10, unique=True)
    
    
    name = fields.Char(string="Teacher Name En", required=True)
    ar_name = fields.Char(string="Teacher Name Ar", required=False)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], required=True, help='Choose the Teacher gender')

    phone = fields.Char(string='Teacher Phone', help='Enter Teacher Phone', required=True)
    mobile = fields.Char(string='Teacher Mobile', help='Enter Teacher Mobile', required=True)
    email = fields.Char(string='Teacher Email', help='Enter Teacher Email', required=True)
    department_id = fields.Many2one('hr.department', 'Department',help='Select department', required=False)

    nationality = fields.Selection([
        ('Saudi', 'Saudi'),
        ('NonSaudi', 'Non Saudi'),
    ], required=True, help='Choose the Teacher nationality')

    website = fields.Char(string='Website', help='Enter teacher website')


    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], readonly=True, default="draft", help='Choose the class state')
    
    note = fields.Text(string="Description")

    
    class_id = fields.One2many('teacher_tabel_line','teacher_id', string="Classes",
                                help='Select class',  required=False)

    studentID = fields.Many2many('student', string="Students", required=False)

    subject_id = fields.Many2many('subject', string="Course-Subjects",help='Select subject',  required=False)

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Teacher'
        if vals.get('teacherID', ('New')) == ('New'):
            vals['teacherID'] = self.env['ir.sequence'].next_by_code('teacher') or ('New')
        res = super(teacher, self).create(vals)
        return res

    @api.constrains('teacher_nat_id')
    def _check_National_ID(self):
       
        new_teacher_nat_id = self.teacher_nat_id
        
        for old_id in self.search([('id', 'not in', self.ids)]):
            # Check start date should be less than stop date
            if (old_id.teacher_nat_id == self.teacher_nat_id ):
                raise ValidationError(_(
                    "Error! You cannot define same ID."))

    

#Address

    assisment_num = fields.Char(string="Assignment Count", compute="compute_assisment")

    def compute_assisment(self):
        for rec in self:
            fee = self.env["teacherassig"].search_count([('teacher_id', '=', self.name)])
            rec.assisment_num = fee

    def action_open_assisment(self):
        domain = [
            ('teacher_id', '=', self.name)]
        return {
            'name': _('Teacher Assignment'),
            'domain': domain,
            'res_model': 'teacherassig',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'target': 'current'
        }

    table_num = fields.Char(string="Table Count", compute="compute_table")

    def compute_table(self):
        for rec in self:
            fee = self.env["teachertable"].search_count(['&',('teacher_id', '=', self.name),('state','=','confirm')])
            rec.table_num = fee

    def action_open_table(self):
        domain = ['&',
            ('teacher_id', '=', self.name),('state','=','confirm')]
        return {
            'name': _('Teacher Table'),
            'domain': domain,
            'res_model': 'teachertable',
            'type': 'ir.actions.act_window',
            'view_mode': 'calendar,tree,form',
            'view_type': 'form',
            'target': 'current'
        }

    compute_field = fields.Boolean(string="check field", compute='get_user')
    evaluation_num = fields.Char(string="Evaluation Count", compute="compute_evaluation")

    def compute_evaluation(self):
        for rec in self:
            evaluation = self.env["evaluation"].search_count([('teacher_id', '=', self.name)])
            rec.evaluation_num = evaluation

    def action_open_evaluation(self):
        domain = [
            ('teacher_id', '=', self.name)]
        return {
            'name': _('Student Evaluation'),
            'domain': domain,
            'res_model': 'evaluation',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'target': 'current'
        }

    @api.depends('compute_field')
    def get_user(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('kb_Tahtheeb_school.group_school_teacher'):
            self.compute_field = True
        else:
            self.compute_field = False