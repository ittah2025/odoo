
from odoo import api, fields, models, _
from logging import getLogger


class damager_report(models.Model):
    _name = "damages_report"
    _table = "damages_report"
    _inherit = ['mail.thread','mail.activity.mixin']

 
    # Damages checklist box 
    JLR = fields.Boolean('Jack & Lever Rod', groups='base.group_user')
    TK = fields.Boolean('Tools kit', groups='base.group_user')
    tri = fields.Boolean('Triangle', groups='base.group_user')
    fireExt =  fields.Boolean('Fire Extinguisher', groups='base.group_user')
    FKB = fields.Boolean('First Aid Kit', groups='base.group_user')
    tandM = fields.Boolean('Tape & Mic', groups='base.group_user')
    spareT = fields.Boolean('Spare Tire', groups='base.group_user')
    chBox = fields.Boolean('Chock Box', groups='base.group_user')
    APG = fields.Boolean('Air Pressure Gauge', groups='base.group_user')
    RgCard = fields.Boolean('Original Registration Card', groups='base.group_user')

    # DATE
    date_2 = fields.Date(string="Date")
    # customer ID 
    # partner_id = fields.Many2one('res.partner', string="Customer", required=True)

    # link to damage_tree.py display tree 
    damage_ids = fields.One2many('damage_tree','damgggg_id', string="damegs")



    # car_id = fields.Many2one('cars', string="Cars", domain="[('partner_id', '=', partner_id)]")

    
    # carMake = fields.Selection(related='car_id.carMake')
    carMake= fields.Char('MAke', groups='base.group_user')
    # carModel = fields.Char(related='car_id.carModel')
    carModel= fields.Char('model', groups='base.group_user')
    # carPlate = fields.Char(related='car_id.carPlate')
    carPlate= fields.Char('plate', groups='base.group_user')
    # carYear = fields.Char(related='car_id.carYear')
    carYear= fields.Char('year', groups='base.group_user')
    # carVin = fields.Char(related='car_id.carVin')
    carVin= fields.Char('vin', groups='base.group_user')
    # CarMilage = fields.Char(related='car_id.CarMilage')
    CarMilage= fields.Char('km', groups='base.group_user')

    # add photo to order
    attachment_id_damage = fields.Many2many('ir.attachment', 'rental_id', 'attachment_id', string="Attachments")
    driver_name = fields.Char('Driver name', groups='base.group_user')
