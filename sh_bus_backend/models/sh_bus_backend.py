# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class AvialbleSeatSelection(models.Model):
    _name = 'available.seat.selection'
    _description = "Available Seat"

    name = fields.Char("Seat Column")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Seat Already exist !')
    ]


class BusSeatingArrangement(models.Model):
    _name = 'bus.seat.arrangement'
    _description = "Arrangement of Seat"

    bus_type_id = fields.Many2one('sh.bus.type', string="Ticket Type")
    row = fields.Integer("Row No")
    sequence = fields.Integer(string='Sequence', default=1)
    seat_selection_ids = fields.Many2many(
        'available.seat.selection', string="Column Selection")


class ShBusType(models.Model):
    _name = "sh.bus.type"
    _description = "Bus Type"

    name = fields.Char('Name')
    layout = fields.Selection([('2-2', '2-2'), ('1-1', '1-1'), ('2-1', '2-1'), ('1-2', '1-2'), ('3-2', '3-2'), ('2-3', '2-3')],
                              string='Layout')
    row_count = fields.Integer("Row")
    col_count = fields.Integer("Column")
    sequence = fields.Integer(string='Sequence', default=10)
    seat_arrangement_ids = fields.One2many(
        'bus.seat.arrangement', 'bus_type_id', string="Bus Seat Arrangement")

    @api.onchange('layout')
    def onchange_layout(self):
        if self.layout:
            if self.layout == '2-2':
                self.col_count = 4
            elif self.layout == '1-1':
                self.col_count = 2
            elif self.layout == '2-1':
                self.col_count = 3
            elif self.layout == '1-2':
                self.col_count = 3
            elif self.layout == '3-2':
                self.col_count = 5
            elif self.layout == '2-3':
                self.col_count = 5

    def clear_arrangement(self):
        self.ensure_one()
        self.seat_arrangement_ids.unlink()

    def prepare_arrangement(self):

        i = 1

        j = 1

        data_list = []
        for row in range(self.row_count):
            row_dic = {}
            col_list = []
            j = 1
            for col in range(self.col_count):
                seat_avail = self.env['available.seat.selection'].sudo().search(
                    [('name', '=', j)], limit=1)
                if not seat_avail:
                    seat_avail = self.env['available.seat.selection'].sudo().create({
                        'name': j})
                col_list.append(seat_avail.id)
                j += 1
            row_dic['row'] = i
            row_dic['seat_selection_ids'] = [(6, 0, col_list)]
            i += 1
            data_list.append((0, 0, row_dic))
        self.seat_arrangement_ids = data_list


class ShBusAmenities(models.Model):
    _name = "sh.bus.amenities"
    _description = "Bus Amenities"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")


class ShBusPoint(models.Model):
    _name = "sh.bus.point"
    _description = "Bus Point"

    name = fields.Char(string="Bus Point Name", required="1")
    point_ids = fields.Many2many(
        "sh.location.point", 'point_id', string="Points(Dropping/Boarding)")


class ShLocationPoint(models.Model):
    _name = "sh.location.point"
    _description = "Location Point"

    name = fields.Char(string="Point Name", required="1")


class ShBusBrand(models.Model):
    _name = "sh.bus.brand"
    _description = "Bus Brand"

    name = fields.Char(string="Brands Name")


class ShRouteManagement(models.Model):
    _name = "sh.route.management"
    _description = "Route Management"

    name = fields.Char(string="Route Number", readonly=True,
                       required=True, copy=False, default='New')
    fleet_id = fields.Many2one("fleet.vehicle", string="Bus")
    baording_id = fields.Many2one("sh.bus.point", string="Boarding Point")
    dropping_id = fields.Many2one("sh.bus.point", string="Dropping Point")
    str_time = fields.Float('Start Time')
    end_time = fields.Float('End Time')
    route_line_ids = fields.One2many(
        'sh.route.line', 'route_line', string='Route Lines', required=True)
    special_price_ids = fields.One2many(
        'sh.special.price', 'route_id', string="Special Price")

    @api.onchange('str_time', 'end_time', 'fleet_id')
    def onchange_time(self):
        if self.str_time and self.end_time:
            if self.str_time >= self.end_time:
                raise UserError(_("End Time must be grater than Start Time !"))
        if self.str_time and self.fleet_id:
            existing_route = self.env['sh.route.management'].sudo().search(
                [('str_time', '<', self.str_time), ('end_time', '>', self.str_time), ('fleet_id', '=', self.fleet_id.id)])
            if existing_route:
                raise UserError(_("Route already Exist !"))
        if self.end_time and self.fleet_id:
            existing_route = self.env['sh.route.management'].sudo().search(
                [('str_time', '<', self.end_time), ('end_time', '>', self.end_time), ('fleet_id', '=', self.fleet_id.id)])
            if existing_route:
                raise UserError(_("Route already Exist !"))

    def get_price(self, from_loc, to_loc):
        price = 0.0
        special_price_line = self.env['sh.special.price'].sudo().search(
            [('route_id', '=', self.id), ('bording_from', '=', from_loc.id), ('to', '=', to_loc.id)], limit=1)
        if special_price_line:
            price = special_price_line.price
        else:
            start_route_line = self.env['sh.route.line'].sudo().search(
                [('route_line', '=', self.id), ('bording_from', '=', from_loc.id)], limit=1)
            end_route_line = self.env['sh.route.line'].sudo().search(
                [('route_line', '=', self.id), ('to', '=', to_loc.id)], limit=1)

            if start_route_line and end_route_line:
                route_lines = self.env['sh.route.line'].sudo().search(
                    [('id', '>=', start_route_line.id), ('id', '<=', end_route_line.id), ('route_line', '=', self.id)])
                if route_lines:
                    for route_line in route_lines:
                        price += route_line.price
        return price

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sh.route.management') or 'New'

        result = super(ShRouteManagement, self).create(vals)
        return result


class ShRouteLine(models.Model):
    _name = "sh.route.line"
    _description = "Route Line"

    bording_from = fields.Many2one(
        'sh.bus.point', string="From", required=True)
    to = fields.Many2one('sh.bus.point', string="To", required=True)
    start_times = fields.Float('Start Time', required=True)
    end_times = fields.Float('End Time', required=True)
    price = fields.Float('Price', required=True)
    route_line = fields.Many2one(
        'sh.route.management', string='Route Line', required=True)


class ShRouteSpecialPrice(models.Model):
    _name = "sh.special.price"
    _description = "Special Price"

    bording_from = fields.Many2one(
        'sh.bus.point', string="From", required=True)
    to = fields.Many2one('sh.bus.point', string="To", required=True)
    price = fields.Float('Price', required=True)
    route_id = fields.Many2one(
        'sh.route.management', string='Route', required=True)


class BookedSeat(models.Model):
    _name = 'bus.booked.seat'
    _description = "Booked Seat"

    name = fields.Char("Booked Seat")
    seat_no = fields.Char("Booked Seat No", compute='get_seat_no')
    seat_id = fields.Char("seat_id")

#     event_ticket_id = fields.Many2one('event.event.ticket',string="Ticket Type")
    bus_id = fields.Many2one('sh.bus.trip', string="Trip")
    search_id = fields.Many2one('sh.bus.search.result', string="trip")

    @api.depends('seat_id')
    def get_seat_no(self):
        for rec in self:
            rec.seat_no = ''
            if rec.seat_id:
                rec.seat_no = 'R' + \
                    rec.seat_id.split('_')[0]+' S'+rec.seat_id.split('_')[1]


class ShBusTrip(models.Model):
    _name = 'sh.bus.trip'
    _description = "Bus trip"

    name = fields.Char(string="Trip Number", readonly=True,
                       required=True, copy=False, default='New')
    route = fields.Many2one('sh.route.management', string="Route")
    bus_id = fields.Many2one("fleet.vehicle", string="Bus")
    trip_date = fields.Date(string="Trip Date")
    total_seat = fields.Integer(
        string="Total Seats", compute='get_seat_calculation')
    seat_booked = fields.Integer(
        string="Seat Booked", compute='get_seat_calculation')
    remaining_seats = fields.Integer(
        string="Remaining Seats", compute='get_seat_calculation')
    booked_seat_ids = fields.One2many(
        'bus.booked.seat', 'bus_id', string="Booked Seat List")
    bording_from = fields.Many2one(
        'sh.bus.point', string="From", related='route.baording_id')
    to = fields.Many2one('sh.bus.point', string="To",
                         related='route.dropping_id')
    trip_start_time = fields.Float(
        string="Start Time", related='route.str_time')
    trip_end_time = fields.Float(string="Stop Time", related='route.end_time')
    booked_seat = fields.Integer("Booked Seat", compute='get_booked_seat')

    def get_booked_seat(self):
        for rec in self:
            rec.booked_seat = self.env['sale.order.line'].sudo().search_count(
                [('trip_id', '=', rec.id), ('booking_status', 'in', ['confirm', 'check_in'])])

    def action_open_booked_seat(self):
        view_id = self.env.ref('sale.view_order_line_tree').id
        so_list = []
        for so_line in self.env['sale.order.line'].sudo().search([('trip_id', '=', self.id)]):
            so_list.append(so_line.id)

        return {
            'name': _("Booked Seat"),
            'view_mode': 'tree',
            'view_id': view_id,
            'res_model': 'sale.order.line',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('id', 'in', so_list)],
        }

    def get_seat_calculation(self):
        for rec in self:
            rec.total_seat = 0
            rec.seat_booked = 0
            rec.remaining_seats = 0
            if rec.bus_id and rec.bus_id.fleet_type and rec.bus_id.fleet_type.col_count > 0 and rec.bus_id.fleet_type.row_count > 0:
                rec.total_seat = rec.bus_id.fleet_type.col_count * rec.bus_id.fleet_type.row_count
                rec.seat_booked = len(rec.booked_seat_ids)
                rec.remaining_seats = rec.total_seat - rec.seat_booked

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sh.bus.trip') or 'New'
        result = super(ShBusTrip, self).create(vals)
        return result


class ShBusSearchResult(models.Model):
    _name = 'sh.bus.search.result'
    _description = "Search Result"

    name = fields.Char(string="Trip Number", readonly=True,
                       required=True, copy=False, default='New')
    route = fields.Many2one('sh.route.management', string="Route")
    bus_id = fields.Many2one("fleet.vehicle", string="Bus")
    trip_date = fields.Date(string="Trip Date")
    trip_start_date = fields.Float(string="Start Time")
    trip_end_date = fields.Float(string="Stop Time")
    total_seat = fields.Integer(
        string="Total Seats", related='trip_id.total_seat')
    seat_booked = fields.Integer(
        string="Seat Booked", related='trip_id.seat_booked')
    remaining_seats = fields.Integer(
        string="Remaining Seats", related='trip_id.remaining_seats')
    booked_seat_ids = fields.One2many(
        'bus.booked.seat', 'search_id', string="Booked Seat List")
    price = fields.Float("Price")
    bording_from = fields.Many2one(
        'sh.bus.point', string="From", required=True)
    to = fields.Many2one('sh.bus.point', string="To", required=True)
    trip_id = fields.Many2one('sh.bus.trip')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sh.bus.search.result') or 'New'
        result = super(ShBusSearchResult, self).create(vals)
        return result

    def clear_data(self):
        today = datetime.today()
        week_ago = today - timedelta(days=7)
        for data in self.search([('create_date', '<=', week_ago)]):
            if data:
                data.unlink()
