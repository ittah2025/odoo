from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime, timedelta
_logger = logging.getLogger(__name__)


class car_dashboard(models.Model):
    _name = 'car_dashboard'
    _description = 'Dashboard Kanban'

    name = fields.Char("Name")

    no_cars = fields.Integer(string="", compute="_onchange_cars")
    no_order_done = fields.Integer(string="", compute="_onchange_order_done")
    no_order_parts = fields.Integer(string="", compute="_onchange_order_parts")
    no_order_going = fields.Integer(string="", compute="_onchange_order_going")
    no_order_onHold = fields.Integer(string="", compute="_onchange_order_onHold")


    def _onchange_cars(self):
        cars = self.env['cars'].search([])
        x = 0
        for carss in cars:
            x += 1
        
        self.no_cars = x
        # raise ValidationError(_(self.no_cars))

    def _onchange_order_done(self):
        order = self.env['orders'].search([])
        x = 0
        for orders in order:
            if orders.state == 'complete':
                x += 1
        
        self.no_order_done = x
        # raise ValidationError(_(self.no_cars))
        
    def _onchange_order_parts(self):
        order = self.env['orders'].search([])
        x = 0
        for orders in order:
            if orders.state == 'order_parts':
                x += 1
        
        self.no_order_parts = x
        # raise ValidationError(_(self.no_cars))

    def _onchange_order_going(self):
        order = self.env['orders'].search([])
        x = 0
        for orders in order:
            if orders.state == 'in_progress':
                x += 1
        
        self.no_order_going = x
        # raise ValidationError(_(self.no_cars))

    def _onchange_order_onHold(self):
        order = self.env['orders'].search([])
        x = 0
        for orders in order:
            if orders.state == 'on_hold':
                x += 1
        
        self.no_order_onHold = x
        # raise ValidationError(_(self.no_cars))
