from decorator import append
from wheel.metadata import requires_to_requires_dist

from odoo import api, fields, tools, models, _
from datetime import datetime
from odoo.exceptions import ValidationError


# Created by Sukainah

class maintenanceForm(models.Model):
    _name = 'kb.maintenance.form'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Maintenance Form"
    _rec_name = 'kb_ordersID'

    kb_ordersID = fields.Char(string='Order ID', required=True,
                              copy=False, readonly=True, default=lambda self: _('Draft'))
    note = fields.Char()
    kb_createdBy = fields.Many2one("res.users", string='Created By', default=lambda self: self.env.user, readonly=True)
    kb_completedBy = fields.Char(string='Completed By', traking=True)
    kb_userID = fields.Many2one('hr.employee', string='Responsible', traking=True, related='kb_building.kb_building_admin')
    # kb_responsible = fields.Char(string='Responsible', traking=True)

    kb_orderDate = fields.Datetime(string='Order Date', traking=True, default=datetime.now())

    # raise ValidationError(_("{} after the for\n").format(kb_orderDate))

    kb_building = fields.Many2one('kb.building.info', string='Building Name')
    # kb_floor = fields.Many2one('building_rooms', string="Floor")

    kb_room = fields.Many2one('floor_details', string="Room")

    kb_floor = fields.Selection([
        ('1', '1'),
        ('3', '2'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
    ], string='Floor')

    kb_expected_cost = fields.Float(string="Expected Cost")

    # @api.onchange('kb_building')
    # def onchange_building(self):
    #     for rec in self.kb_building:
    #         return {'domain': {'kb_floor': [('kb_floor', '=', rec.kb_floor)]}}

    #
    @api.onchange('kb_floor')
    def kb_get_room_from_table(self):
        if self.kb_building and self.kb_floor:
            id_list = []
            count_ids = self.env['building_rooms'].search(
                    [('kb_building', '=', self.kb_building.id), ('kb_floor', '=', self.kb_floor)], limit=1)
            for x in count_ids:
                for rec in x.kb_floor_details_ids:
                    id_list.append(rec.id)
            return {'domain': {'kb_room': [('id', 'in', id_list)]}}



    kb_note = fields.Text(string='', required="True")

    kb_state = fields.Selection([
        ('draft', 'Draft'),
        ('completeForm', 'Complete Form'),
        ('waiting', 'Waiting for Approval'),
        ('approval', 'Approval'),
        ('inProgress', 'In Progress'),
        ('done', 'Done'),
        ('reject', 'Reject'),
    ], readonly=True, default="draft", help='Choose the state', string='Status', traking=True)

    kb_rejection_date = fields.Datetime(string="Reject Date", traking=True)
    kb_reject_by = fields.Many2one(
            'res.users', string="Reject By", default=lambda self: self.env.user)
    kb_reject_reason = fields.Char(string="Reject Reason", traking=True)

    kb_maintenanceFormID = fields.One2many('kb.maintenance.form.line', 'kb_maintenanceFormLineID', string='')

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Order'
        if vals.get('kb_ordersID', ('New')) == ('New'):
            vals['kb_ordersID'] = self.env['ir.sequence'].next_by_code(
                    'ordersID.seq') or ('New')
        res = super(maintenanceForm, self).create(vals)
        return res

    def complete_order_in_maintenance(self):
        self.write({'kb_state': 'completeForm'})
        group_complete_form = self.env.ref('kb_school_maintenance.group_complete_form').users
        for users in group_complete_form:
            print(f"userr  ==> {users.id}")
            self.activity_schedule('mail.mail_activity_data_todo', user_id=users.id,
                                   note=f'There is a new Maintenance Orders with name: {self.kb_ordersID}')

    def waiting_approval_maintenance_form(self):
        self.write({'kb_state': 'waiting'})
        group_approval_form = self.env.ref('kb_school_maintenance.group_approval_form').users
        for users in group_approval_form:
            print(f"userr  ==> {users.id}")
            self.activity_schedule('mail.mail_activity_data_todo', user_id=users.id,
                                   note=f'There is a new Maintenance Orders with name: {self.kb_ordersID}')

    def approval_maintenance_form(self):
        for rec in self:
            rec.kb_state = 'approval'


class maintenanceFormLin(models.Model):
    _name = 'kb.maintenance.form.line'

    kb_description = fields.Char(string='Description', traking=True)
    kb_maintenanceType = fields.Many2one('kb.maintenance.type', string='Maintenance Type', traking=True)
    doc_attachment_ids8 = fields.Many2many('ir.attachment', 'doc_attach_rels8', 'doc_ids', 'attach_id5',
                                           string="Attachment",
                                           help='You can attach the copy of your document', copy=False, traking=True)

    kb_maintenanceFormLineID = fields.Many2one('kb.maintenance.form', string='')

    Note = fields.Char(string="Note")

# class Attachment(models.Model):
#     _inherit = 'ir.attachment'

#     doc_attach_rels8 = fields.Many2many('document.fields', 'doc_attachment_ids8', 'attach_id5', 'doc_ids', string="Attachment", invisible=1)
