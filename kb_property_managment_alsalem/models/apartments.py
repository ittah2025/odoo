from odoo import api, fields, models
from datetime import date, timedelta
from odoo.exceptions import UserError
from odoo import _

class Apartments(models.Model):
    _name = "apartments"
    _rec_name = 'name'

    name = fields.Char(string="Name")
    bathroom = fields.Char(string="Bathroom Number")
    room_id = fields.One2many('rooms', 'aprtment_id', string='Room lines')
    property_id = fields.Many2one('property')
    final_total_apartment =  fields.Float(string="Total",  readonly= True , compute="calculat_total_final_apartment" )

    # calculate final total of Apartments 
    @api.depends('final_total_apartment')
    def calculat_total_final_apartment(self):
        total= 0 
        for t in self.room_id:
            total += t.cost
        self.final_total_apartment = total
    
class ApartmmentsInherited(models.Model):
    _inherit = "apartments"

    def maintenance_count(self):
        for each in self:
            maintenance_ids = self.env['maintenance'].search([('property_unit', '=', each.id)])
            each.maintenance_countss = len(maintenance_ids)

    def return_action_to_maintenance(self):
        self.ensure_one()
        domain = [
            ('property_unit', '=', self.id)]
        return {
            'name': _('maintenance'),
            'domain': domain,
            'res_model': 'maintenance',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                           Click to Create for New service
                        </p>'''),
            'limit': 80,
            'context': "{'default_property_unit': '%s'}" % self.id,
        }
    maintenance_countss = fields.Integer(compute='maintenance_count', string='# maintenance')

    def rooms_count(self):
        for each in self:
            room_view_ids = self.env['contract'].search([('room_ids', '=', each.id)])
            each.room_view_countss = len(room_view_ids)

    def return_action_to_view_room(self):
        self.ensure_one()
        domain = [
            ('room_ids', '=', self.id)]
        return {
            'name': _('Room'),
            'domain': domain,
            'res_model': 'contract',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                           Click to Create for New service
                        </p>'''),
            'limit': 80,
            'context': "{'default_room_ids': '%s'}" % self.id,
        }
    room_view_countss = fields.Integer(compute='rooms_count', string='# Contract')

class Rooms(models.Model):
    _name = "rooms"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string="name")
    cost = fields.Float(string="Cost Of the room")
    bathroom = fields.Selection([
        ('private', 'Private'),
        ('shared', 'Shared'),
    ], default="private")
    aprtment_id = fields.Many2one('apartments')
   

    rented_room = fields.Boolean(string="Rented" ,default=False)

    
    inv_id = fields.Char(string='INV No ', required=True,
                            copy=False, readonly=True, default=lambda self: _('New'))
    note3 = fields.Char()


    @api.model
    def create(self, vals):
        if not vals.get('note3'):
            vals['note3'] = 'New Room'
        if vals.get('inv_id', ('New')) == ('New'):
            vals['inv_id'] = self.env['ir.sequence'].next_by_code(
                'room.seq') or ('New')
        res = super(Rooms, self).create(vals)


        id_product = self.env['product.template']
        valu  = {
            'name': vals.get('name'),
            'standard_price':0.00,
            'list_price': vals.get('cost'),
            'type': 'consu',
            'categ_id': 1,
            }
        product_ids = id_product.create(valu)
        if product_ids:
            self.write({'id':product_ids.id})
        return res




class Transportation(models.Model):
    _name = "transportation"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # name = fields.Char(string="name")
    customer_id = fields.Many2one('res.partner', 'Tenant Data')
    price = fields.Integer(string="Price" , default=10 , readonly=True)
    train_station= fields.Selection([
        ('going', 'الذهاب '),
        ('back', 'العودة'),
     
    ], string='المواصلات لمحطة القطار')

    date_of = fields.Datetime(string="Date")    