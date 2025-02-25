
from odoo import api, fields, models, _
from logging import getLogger
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime, timedelta
_logger = logging.getLogger(__name__)


class fleet_new(models.Model):
    
    _inherit = "fleet.vehicle"

    busNameAR = fields.Char('Bus Name Arabic')
    busNameEN = fields.Char('Bus Name English')
    searialNumbers = fields.Char('Serial Number')
    plateNumberAR = fields.Char('Plate Number (Arabic)')
    ownerName = fields.Char('Owner Name')
    electronicNumer = fields.Char('Operating Code Number')
    insuranceName = fields.Char('Insurance Name')
    insuranceStartDate = fields.Date('Insurance Start Date')
    insuranceEndDate = fields.Date('Insurance End Date')
    insuranceStatus = fields.Selection([
        ('run', 'Running'),
        ('Expired', 'Expired'),
    ], string='Insurance Status')
    insurancePrice = fields.Char('Insurance Price')
    modelYear = fields.Char('Model Year')
    passengerCapacity = fields.Char('Passenger Capacity')
    registrationEndDate = fields.Date('Registration Expiration Date')
    fleetAttachment = fields.Many2many('ir.attachment', string="Attachments")
    ownerElectronicumber = fields.Char('Electronic Owner Number')
    status_field = fields.Char('Vehicle Status')
    customFormNumber = fields.Char("Custom Card Number")
    customDate = fields.Date("Custom Date")
    customSource = fields.Char("Custom Source")
    InspectionDate = fields.Date("Periodic Inspection Expiration Date")
    oprCardNumber = fields.Char("Operations Card Number")
    oprCardStart = fields.Date("Operations Card Start Date")
    oprCardEnd = fields.Date("Operations Card End Date")
    colorVh = fields.Char("Color")

    engineOil = fields.Char("Engine Oil Type")
    oil_filter = fields.Char("Oil Filter")
    oilCapacityOf = fields.Char("Engine Oil Capacity Without Filter")
    oilCapacityWf = fields.Char("Engine Oil Capacity With Filter")
    oil_serv_km = fields.Float("Engine Oil change Every (Km)")
    oil_filter_serv_km = fields.Float("Oil Filter change Every (Km)")




    transOil = fields.Char("transmission Oil Type")
    transcapacity = fields.Char("transmission Oil Capacity")
    trans_serv_km = fields.Float("Transmission Oil change Every (Km)")

    diffOil = fields.Char("Differential Oil Type")
    diffoilCapacity = fields.Char("Differential Oil Capacity")
    diffoil_serv_km = fields.Float("Differential Oil change Every (Km)")

    engineFilter = fields.Float("Air Filter (Km)")
    engineBelts = fields.Float("Engine Belts (Km)")
    tirelife = fields.Float("Tires (Km)")
    batterylife = fields.Float("Battery")
    brakes = fields.Float("Brakes (Km)")
    acFilters = fields.Float("AC Filter (Km)")

    # date_table_id123 = fields.One2many('dates_table', 'datesTable_id_1')

        



class VehicleModelsNew(models.Model):
    _inherit = "fleet.vehicle.model"

    vehicle_type = fields.Selection(selection_add=[('bus', 'BUS'), ('COSTAR', 'COSTAR')], ondelete={'bus': 'set default', 'COSTAR': 'set default'})
    # vehicle_type = fields.Selection([('car', 'Car'), ('bike', 'Bike')], default='car', required=True)

   
