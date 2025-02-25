from odoo import api, fields, tools, models, _


class BuildingRooms(models.Model):
    _name = 'building_rooms'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'kb_floor'


    kb_building = fields.Many2one('kb.building.info', string="Building")
    # kb_floor = fields.Many2one('floors', string="Floor")

    kb_floor = fields.Selection([
        ('1', '1'),
        ('3', '2'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
    ], string='Floor')

    kb_floor_details_ids = fields.One2many('floor_details', 'kb_floor_details_id')






class buildingFloors(models.Model):
    _name = 'floors'


    name = fields.Char(string="Floor")




class BuildingFloorDetails(models.Model):
    _name = 'floor_details'
    _rec_name = 'kb_name'



    kb_name = fields.Char(string="Room Name")
    kb_type = fields.Many2one('room_type', string="Type")

    kb_floor_details_id = fields.Many2one('building_rooms', string="building_rooms id")


class RoomsTypes(models.Model):
    _name = 'room_type'


    name = fields.Char(string="Type")