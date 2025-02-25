
from odoo import api, fields, models, _
from logging import getLogger
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime, timedelta
_logger = logging.getLogger(__name__)


class fleet_new(models.Model):
    
    _inherit = "fleet.vehicle"

    # @Fatimah00J
    kb_num_passengers = fields.Integer("Number of passengers")
    kb_num_cylinders = fields.Integer("Number of cylinders")
    kb_expected_life= fields.Integer("Expected life of the car")
    kb_side_number = fields.Integer("Side number")
    kb_fuel_type = fields.Selection([('gasoline','Gasoline'),('diesel','Diesel')]
                                    ,"Type of the fuel")

    kb_vehicle_type = fields.Selection([('owned','Owned'),('rented','Rented')]
                                    ,"Type of the vehicle")

    kb_customs_card = fields.Char("Customs Card ")
    kb_color= fields.Char("Color of car/bus")
    kb_tire_size= fields.Char("Tire size")
    kb_tire_number= fields.Char("Number of Tire")
    doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Number of documents attached")
    end_assignation_date=fields.Date("End Date of assignation ")
    
    kb_plate_number_ar = fields.Char(string="Plate Name (AR)")
    kb_vehicle_ar = fields.Char(string="Vehicle Name (AR)")

    kb_registration_type = fields.Many2one(comodel_name="registration_type", string="Registration Type",)

    kb_serial_number = fields.Char(string="Serial Number")

    kb_manufacturer = fields.Many2one(comodel_name="res.country", string="Manufacturer")
    kb_vehicle_weight = fields.Char(string="Vehicle Weight")
    
    
    kb_vehicle_ar = fields.Char(string="Vehicle Name (AR)")
    kb_vehicle_en = fields.Char(string="Vehicle Name (En)")
    
    kb_owner_name = fields.Char(string="Owner Name")
    kb_owner_id = fields.Char(string="Owner ID")
    
    

    kb_weight_unit = fields.Selection([
        ('kilometers', 'km'),
        ('miles', 'mi')
    ], string='Odometer Unit', default='kilometers')
    
    
    def _compute_attached_docs_count(self):
        Attachment = self.env['ir.attachment']
        for project in self:
            project.doc_count = Attachment.search_count([
                '&',
                ('res_model', '=', 'fleet.vehicle'), ('res_id', '=', project.id),
            ])
    def kb_documment_create(self):
        action = self.env['ir.actions.act_window']._for_xml_id('base.action_attachment')
        action['domain'] = str([
            '&',
            ('res_model', '=', 'fleet.vehicle'),
            ('res_id', 'in', self.ids),
        ])
        action['context'] = "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        return action

    @api.model
    def create_driver_history(self, vals):
        last_ids = self.env['fleet.vehicle.assignation.log'].search([])
        if last_ids:
            last_id = self.env['fleet.vehicle.assignation.log'].search([])[-1]
            for last in last_id:
                if not last.date_end:
                    last_id.unlink()
        res = super(fleet_new, self).create_driver_history(vals)
        return res

    @api.model
    def _get_driver_history_data(self, vals):
        self.ensure_one()
        return {'vehicle_id': self.id,
                'driver_id': vals['driver_id'],
                'date_start': self.next_assignation_date,
                'date_end': self.end_assignation_date,
            }


class kb_ir_attachment_fleet(models.Model):
    _inherit = 'ir.attachment'



class KbRegistrationType(models.Model):
    _name = 'registration_type'
    _rec_name = "kb_name"


    kb_name = fields.Char(string='Name')
