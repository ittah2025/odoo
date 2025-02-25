
from odoo import api, fields, models, _
from logging import getLogger
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime, timedelta
_logger = logging.getLogger(__name__)


class accidents(models.Model):

    _name = "accidents"
    _table = "accidents"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    electronicNumer_accd = fields.Char("Operating Code Number")
    accidentsDescription = fields.Text("Accident Description")
    accidentsDate = fields.Date("Date of Accidents")
    accidentsAttachment = fields.Many2many('ir.attachment', string="Attachments")
    accidentNumber = fields.Char("Accident Number")
    driver_name = fields.Many2many('hr.employee', string="Drivers Name")
    accidentsStatus = fields.Char("Accident Status")
    ############################### Vehicle from fleet Module#######################################################################
    
    carModel_acc = fields.Char("Model")
    # busNameAR_acc = fields.Char("Bus Name Arabic")
    # busNameEN_acc = fields.Char("Bus Name English")
    searialNumbers_acc = fields.Char("Serial Number")
    plateNumberAR_acc = fields.Char("Plate Number (Arabic)")
    ownerName_acc = fields.Char("Owner Name")
    electronicNumer_acc = fields.Char("Operating Code Number")
    insuranceName_acc = fields.Char("Insurance Name")
    insuranceStartDate_acc = fields.Date("Insurance Start Date")
    insuranceEndDate_acc = fields.Date("Insurance End Date")
    modelYear_acc = fields.Char("Model Year")
    passengerCapacity_acc = fields.Char("Passenger Capacity")
    registrationEndDate_acc = fields.Date("Registration Expiration Date")
    ownerElectronicumber_acc = fields.Char("Electronic Owner Number")
    status_field_acc = fields.Char("Vehicle Status")


    @api.onchange('electronicNumer_accd')
    def _get_vehicle_info(self):
        fleet_id = self.env['fleet.vehicle'].search([('electronicNumer', '=', self.electronicNumer_accd)])

        for fleet_ids in fleet_id:
            self.carModel_acc = fleet_ids.model_id.name
            self.modelYear_acc = fleet_ids.modelYear
            # self.busNameAR_acc = fleet_ids.busNameAR
            # self.busNameEN_acc = fleet_ids.busNameEN
            self.searialNumbers_acc = fleet_ids.searialNumbers
            self.ownerName_acc = fleet_ids.ownerName
            self.electronicNumer_acc = fleet_ids.electronicNumer
            self.insuranceName_acc = fleet_ids.insuranceName
            self.insuranceStartDate_acc = fleet_ids.insuranceStartDate
            self.insuranceEndDate_acc = fleet_ids.insuranceEndDate

            self.passengerCapacity_acc = fleet_ids.passengerCapacity
            self.registrationEndDate_acc = fleet_ids.registrationEndDate
            self.ownerElectronicumber_acc = fleet_ids.ownerElectronicumber
            self.status_field_acc = fleet_ids.status_field