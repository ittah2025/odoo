
from odoo import api, fields, models, _
from logging import getLogger


class cars(models.Model):
    _name = "cars"
    # _rec_name = "carPlate"
    _table = "cars"
    _inherit = ['mail.thread','mail.activity.mixin']
# for user to enter car information Make, Model, Plate, Year, and Vin


    # carMake = fields.Char('Make', groups='base.group_user', help='Car Make')
   
    # carMake = fields.Selection([
    #     ('TOYOTA', 'TOYOTA'),
    #     ('FORD', 'FORD'),
    #     ('BMW', 'BMW'),
    # ], string= 'Make', required=True)

    #vehicleSerialNumber = fields.Char('Vehicle Serial Number', groups='base.group_user', required=True)

    carModel = fields.Char('Model', groups='base.group_user', required=True)
    # carPlate = fields.Char('Plate', groups='base.group_user', help='Plate number', required=True)
    
    # carYear = fields.Char('Year', groups='base.group_user', help='Car Year', required=True)

    # carVin = fields.Char('VIN', groups='base.group_user', help='Enter Vin Number')
    # carServ = fields.Char('Service Description', groups='base.group_user', help='Enter Service or issue') 
    # carColor = fields.Char('Color', groups='base.group_user', help='Color') 
    CarMilage = fields.Char('Vehicle Odometer (Km)', groups='base.group_user',required=True)
    uploadImage = fields.Many2many('ir.attachment', string="Image")

# Customer contact info

    # partner_id = fields.Many2one('res.partner', string="Customer", required=True)

    # name = fields.Char(related='car_id')
    # car_id = fields.Char(string='Car  ID', required=True, copy=False, readonly=True,
    #                               index=True, default=lambda self: _('New'))
    # note = fields.Char(string='')
    # @api.model
    # def create(self, vals):
    #     if not vals.get('note'):
    #         vals['note'] = 'New Car'
    #     if vals.get('car_id', ('New')) == ('New'):
    #         vals['car_id'] = self.env['ir.sequence'].next_by_code(
    #             'cars') or ('New')
    #     res = super(cars, self).create(vals)
    #     return res

    
    # def name_get(self):
    #     result = []
    #     for record in self:
    #         record_name = '[' + record.carPlate + '] ' + record.car_id
    #         result.append((record.id, record_name))
    #     return result
