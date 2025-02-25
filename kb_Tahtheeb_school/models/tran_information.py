from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class tran_information(models.Model):
    _name = 'tran_information'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Transport Information'
    _rec_name = 'kb_TransportRoot'

    kb_TransportRoot = fields.Char("Transport Root Name  ")
    kb_ContactPerson = fields.Integer("Contact Person ")
    KB_price = fields.Float("Monthly Price")
    kb_StartDate = fields.Date("Start Date ")
    kb_EndDate = fields.Date("End Date ")
    kb_district = fields.Char("District")
    kb_bus_responsible = fields.Many2one('hr.employee',"Bus responsible")

    academic_id=fields.Many2one('academic_year',string='Academic year')

    kb_VehicleDetails = fields.One2many('tran_vehicle_details','kb_VehicleID',string="")

    trans_participants_ids = fields.One2many("transport_registration",'transportRoot',string=" ")

    kb_recordsCount = fields.Integer(compute="_count_records")

    @api.depends("trans_participants_ids")
    def _count_records(self):
        for rec in self:
            rec.kb_recordsCount = len(rec.trans_participants_ids)

class tran_vehicle_detailss(models.Model):
    _name = 'tran_vehicle_details'
    _description = "Transport Vehicle Details"

    kb_Model = fields.Many2one('fleet.vehicle', 'Model')
    kb_driver = fields.Many2one('res.partner', 'driver', related='kb_Model.driver_id')
    kb_LicensePlate = fields.Char("License Plate",related='kb_Model.license_plate', readonly=True)
    futureDriverId = fields.Many2one('res.partner', string='Future Driver', related='kb_Model.future_driver_id',readonly=True)

    kb_VehicleID = fields.Many2one('tran_information')
