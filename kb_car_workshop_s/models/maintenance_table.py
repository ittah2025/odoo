from odoo import api, fields, models, _
from calendar import month
from email.policy import default
from datetime import date
from datetime import datetime
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime
_logger = logging.getLogger(__name__)


class maintenance_table(models.Model):
    _name = "maintenance_table"




    # maintenanceids_1 = fields.Many2one('maintenanceItems', store=True, string="Title")



    maintenanceTable_id = fields.Many2one('orders')

    total_days_count = fields.Char(string="Total Time")

    # next_service = fields.Float(string="Next Service (Km)", readonly=1)
    next_service = fields.Float(string="Next Service (Km)", compute="_get_km_info")

    # @api.onchange('next_service')
    def _get_km_info(self):
        moves_ids = str(self.maintenanceTable_id.id)
        move_ids = moves_ids.replace("NewId_", "")
        order_km_id = self.env['orders'].search([('id', '=', move_ids)])

        for r in self:
            totals = 0.0
            if r.maintenanceItem == 'Eowoil':
                totals = order_km_id.odometerIN + order_km_id.oil_serv_km_fleet
            elif r.maintenanceItem == 'Ewoil':
                totals = order_km_id.odometerIN + order_km_id.oil_serv_km_fleet
            elif r.maintenanceItem == 'oilfter':
                totals = order_km_id.odometerIN + order_km_id.oil_filter_serv_km_feet
            elif r.maintenanceItem == 'Toil':
                totals = order_km_id.odometerIN + order_km_id.tr_oil_typ_feet
            elif r.maintenanceItem == 'efilter':
                totals = order_km_id.odometerIN + order_km_id.engineFilter_feet
            elif r.maintenanceItem == 'Ebelts':
                totals = order_km_id.odometerIN + order_km_id.engineBelts_feet
            elif r.maintenanceItem == 'Toil':
                totals = order_km_id.odometerIN + order_km_id.tr_oil_typ_feet
            elif r.maintenanceItem == 'acfilter':
                totals = order_km_id.odometerIN + order_km_id.acFilters_feet
            elif r.maintenanceItem == 'tires':
                totals = order_km_id.odometerIN + order_km_id.tirelife_feet
            elif r.maintenanceItem == 'brakes':
                totals = order_km_id.odometerIN + order_km_id.brakes_feet
            r.next_service = totals

        # raise ValidationError(_("{} after the for\n").format(order_km_id.odometerIN))


    maintDescrription = fields.Char(string="Description")


    maintenanceItem = fields.Selection([

        ('Eowoil', 'Engine Oil Without Filter'),
        ('Ewoil', 'Engine Oil With Filter'),
        ('oilfter', 'Oil Filter'),
        ('Toil', 'Transmission Oil'),
        ('efilter', 'Air Filter'),
        ('Ebelts', 'Engine Belts'),

        ('acfilter', 'AC Filter'),
        ('tires', 'Tires'),
        ('brakes', 'Brakes'),

    ], tracking=True)

    installDate = fields.Date("Install Date", groups='base.group_user')
    changeDate = fields.Date("Expiration Date", groups='base.group_user')



    @api.onchange('installDate', 'changeDate', 'total_days_count')
    def calculate_date(self):
           if self.installDate and self.changeDate:
               d1 = datetime.strptime(str(self.installDate), '%Y-%m-%d')
               d2 = datetime.strptime(str(self.changeDate), '%Y-%m-%d')
               self.total_days_count = d2 - d1

    #
    # @api.onchange('changeDate')
    # def check_expr_date(self):
    #     for each in self:
    #         exp_date = each.changeDate
    #         if exp_date and exp_date < date.today():
    #             return {
    #                 'warning': {
    #                     'title': _('Document Expired.'),
    #                     'message': _("Your Document Is Already Expired.")
    #                 }
    #             }