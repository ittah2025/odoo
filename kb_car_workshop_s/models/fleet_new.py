
from odoo import api, fields, models, _
from logging import getLogger
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime, timedelta
_logger = logging.getLogger(__name__)


class fleet_new(models.Model):
    
    _inherit = "fleet.vehicle"

    busNameAR = fields.Char('Bus Name Arabic', required=True)
    busNameEN = fields.Char('Bus Name English', required=True)
    searialNumbers = fields.Char('Serial Number',required=True)
    plateNumberAR = fields.Char('Plate Number (Arabic)', required=True)
    ownerName = fields.Char('Owner Name', required=True)
    electronicNumer = fields.Char('Operating Code Number', required=True)
    insuranceName = fields.Char('Insurance Name', required=True)
    insuranceStartDate = fields.Date('Insurance Start Date', required=True)
    insuranceEndDate = fields.Date('Insurance End Date', required=True)
    insurancePrice = fields.Char('Insurance Price', required=True)
    modelYear = fields.Char('Model Year', required=True)
    passengerCapacity = fields.Char('Passenger Capacity', required=True)
    registrationEndDate = fields.Date('Registration Expiration Date', required=True)
    fleetAttachment = fields.Many2many('ir.attachment', string="Attachments")
    ownerElectronicumber = fields.Char('Electronic Owner Number', required=True)

    # def new_fields(self):
        

#     VehicleModelsNew

class VehicleModelsNew(models.Model):
    
    _inherit = "fleet.vehicle.model"

    vehicleType =  fields.Selection([
     ('car', 'Car'),
     ('bus','Bus'),
   
    ], string= 'Vehicle Type', required=True)
