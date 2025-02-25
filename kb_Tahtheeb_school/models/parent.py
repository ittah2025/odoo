# -*- coding: utf-8 -*-
from email.policy import default
from odoo.exceptions import UserError, ValidationError
#from typing_extensions import Required
from odoo import api, fields, models
from datetime import date
from odoo.tools.translate import _
import re


class parent(models.Model):
    _name = "parent"
    _table = "parent"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Parent Information"

    photo = fields.Binary(
        String='photo', help='Choose the photo')
    name = fields.Char(string="Parent Name", required=True)

    ar_name = fields.Char(string="Parent Name in arabic", required=False)

    parent_nat_id = fields.Char(string="National ID", copy=False, required=True, size=10, unique=True)


    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], required=False, help='Choose the Parent gender')

    phone = fields.Char(string='Parent Phone', help='Enter Parent Phone', required=True)
    mobile = fields.Char(string='Parent Mobile', help='Enter Parent Mobile', required=True)
    email = fields.Char(string='Parent Email', help='Enter Parent Email', required=True)
    nationality = fields.Selection([
        ('Saudi', 'Saudi'),
        ('NonSaudi', 'Non'),
    ], required=True, help='Choose the Parent nationality')


    ParentID = fields.Char(string='Parent ID', required=False,
                            copy=False, readonly=True, default=lambda self: ('New'))
    
    studentID = fields.Many2many('student', string="Students")
    
    childs = fields.Integer(string="Number of Childs", compute="count_childs", required=False)

    relative = fields.Selection([
        ('father', 'Father'),
        ('mother', 'Mother'),
    ], required=False, help='Choose the Parent Relative')



    note = fields.Text(string="Description")
    
    country_id = fields.Many2one('res.country', string='Country', required=False)
    state_id = fields.Many2one('res.country.state', string='State')
    street = fields.Char (string="Street", required=False)
    district = fields.Char (string="District", required=False)
    building_number = fields.Char (string="Building Number")
    city = fields.Char (string="City", required=False)
    postal_code = fields.Char (string="Postal Code")
    extra_number = fields.Char (string="Extra Number")
    is_teacher = fields.Boolean (string="Is teacher")

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Parents'
        if vals.get('ParentID', ('New')) == ('New'):
            vals['ParentID'] = self.env['ir.sequence'].next_by_code(
                'parent') or ('New')
        res = super(parent, self).create(vals)
        # parent_grp_id = self.env.ref('kb_Tahtheeb_school.group_school_parent')
        # emp_grp = self.env.ref('base.group_user')
        # parent_group_ids = [emp_grp.id, parent_grp_id.id]
        # user_obj = self.env['res.users']
        # user_vals = {
        #     'name': self.name,
        #     'email': self.email,
        #     'login': self.email,
        #     'password': str(self.name) + '@' + str(self.parent_nat_id),
        #     'groups_id': [(6, 0, parent_group_ids)],
        #
        # }
        # user_ids = user_obj.create(user_vals)
        # if user_ids:
        #     self.write({'id': user_ids.id,})
        return res

    @api.onchange("studentID")
    def count_childs(self):
        counter = 0
        for i in self.studentID:
            counter = counter + 1
        self.childs = counter

    @api.constrains('parent_nat_id')
    def _check_National_ID(self):
       
        new_parent_nat_id = self.parent_nat_id
        
        for old_id in self.search([('id', 'not in', self.ids)]):
            # Check start date should be less than stop date
            if (old_id.parent_nat_id == self.parent_nat_id ):
                raise ValidationError(_(
                    "Error! You cannot define same ID."))

        teachers_ids = self.env['teacher'].search([('teacher_nat_id','=',self.parent_nat_id)])
        if teachers_ids:    
            # raise ValidationError(_(teachers_ids))
            self.is_teacher = True
        else:
            pass

    compute_field = fields.Boolean(string="check field", compute='get_user')

    @api.depends('compute_field')
    def get_user(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('kb_Tahtheeb_school.group_school_parent'):
                self.compute_field = True
        else:
                self.compute_field = False

        # property_id = self.env['product.product'].search([('is_property','=',True),('name','=',self.name)], limit=1)
    # @api.onchange('studentID')
    # def onchange_student_id(self):
    #     """Onchange Method for Student."""
    #     standard_ids = [student.standard_id.id
    #                     for student in self.studentID]
    #     if standard_ids:
    #         stand_ids = [student.standard_id.standard_id.id
    #                      for student in self.studentID]
    #         self.standard_id = [(6, 0, standard_ids)]
    #         self.stand_id = [(6, 0, stand_ids)]
    # partner_id = fields.Many2one('res.partner', 'User ID', ondelete="cascade",
    #                              delegate=True, required=True,
    #                              help='Partner which is user over here')
    
  

#Address

    # @api.model
    # def create(self, vals):
    #     """Inherited create method to assign values in
    #     the users record to maintain the delegation"""
    #     parent_rec = super(parent, self).create(vals)
    #     parent_grp_id = self.env.ref('kb_div_school.group_school_parent')
    #     emp_grp = self.env.ref('base.group_user')
    #     parent_group_ids = [emp_grp.id, parent_grp_id.id]
    #     user_vals = {'name': parent_rec.name,
    #                  'login': parent_rec.email,
    #                  'email': parent_rec.email,
    #                  'partner_id': parent_rec.partner_id.id,
    #                  'groups_id': [(6, 0, parent_group_ids)]
    #                  }
    #     self.env['res.users'].create(user_vals)
    #     return parent_rec

    # otherparent_nat_id = fields.Char(string="National ID", copy=False, required=False, size=10, unique=True)
    # othergender = fields.Selection([
    #     ('male', 'Male'),
    #     ('female', 'Female'),
    # ], required=False, help='Choose the Parent gender',string="Gender")
    # othernationality = fields.Selection([
    #     ('saudi', 'Saudi'),
    #     ('non', 'Non'),
    # ], required=False, help='Choose the Parent nationality', string='Nationality')
    # otherrelative = fields.Selection([
    #     ('father', 'Father'),
    #     ('mother', 'Mother'),
    # ], required=False, help='Choose the Parent Relative', string='relative')
    #
    # Othermobile = fields.Char(string='Other Parent Mobile', help='Enter Parent Mobile')


    @api.onchange('relative')
    def other_infirnation(self):
        for rec in self:
            if rec.relative=='father':
                rec.otherrelative = 'mother'
                rec.othergender='female'
                rec.gender='male'
            else:
                rec.otherrelative='father'
                rec.othergender ='male'
                rec.gender = 'female'


