# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, _


class BusBoking(models.TransientModel):
    _name = "sh.bus.booking.wizard"
    _description = "Bus Booking wizard"

    date = fields.Date("Journey Date", default=fields.Date.today)
    from_location = fields.Many2one('sh.bus.point', string="From")
    to_location = fields.Many2one('sh.bus.point', string="To")
    fleet_type = fields.Many2one('sh.bus.type', string="Fleet Type")

    def action_search_bus(self):
        if self.date and self.from_location and self.to_location:
            domain = [('bording_from', '=', self.from_location.id)]
            if self.fleet_type:
                domain.append(('route_line.fleet_id.fleet_type',
                               '=', self.fleet_type.id))

            route_line_from = self.env['sh.route.line'].sudo().search(domain)
            # first check from location
            search_ids = []
            if route_line_from:
                for each_line in route_line_from:
                    rid = each_line.route_line.id
                    fleet_id = each_line.route_line.fleet_id.id
                    # get route id and check to location with higher id of that route line
                    route_line_to = self.env['sh.route.line'].sudo().search(
                        [('route_line', '=', rid), ('id', '>=', each_line.id), ('to', '=', self.to_location.id)])

                    if route_line_to:
                        # Bus is available
                        # check in bus trip
                        existing_trip = self.env['sh.bus.trip'].sudo().search([('route', '=', rid), ('trip_date', '=', self.date),
                                                                               ('bus_id', '=', fleet_id)], limit=1)

                        if not existing_trip:
                            existing_trip = self.env['sh.bus.trip'].sudo().create({
                                'route': rid,
                                'trip_date': self.date,
                                'bus_id': fleet_id,

                            })

                        # check in bus search result
                        trips = self.env['sh.bus.search.result'].sudo().search([('route', '=', rid), ('trip_date', '=', self.date),
                                                                                ('bus_id', '=',
                                                                                 fleet_id),
                                                                                ('bording_from', '=',
                                                                                 self.from_location.id),
                                                                                ('to', '=', self.to_location.id)])
                        if trips:
                            for trip in trips:
                                search_ids.append(trip.id)
                                if existing_trip.booked_seat_ids:
                                    for booked_seat_id in existing_trip.booked_seat_ids:
                                        search_bus_id = self.env['bus.booked.seat'].sudo().create({'search_id': trip.id,
                                                                                                   'name': booked_seat_id.name,
                                                                                                   'seat_id': booked_seat_id.seat_id
                                                                                                   })

                        else:
                            result = self.env['sh.bus.search.result'].sudo().create({
                                'route': rid,
                                'trip_date': self.date,
                                'trip_start_date': each_line.start_times,
                                'trip_end_date': route_line_to.end_times,
                                'bus_id': fleet_id,
                                'price': each_line.route_line.get_price(self.from_location, self.to_location),
                                'bording_from': self.from_location.id,
                                'to': self.to_location.id,
                                'trip_id': existing_trip.id
                            })
                            if existing_trip.booked_seat_ids:
                                for booked_seat_id in existing_trip.booked_seat_ids:
                                    search_bus_id = self.env['bus.booked.seat'].sudo().create({'search_id': result.id,
                                                                                               'name': booked_seat_id.name,
                                                                                               'seat_id': booked_seat_id.seat_id
                                                                                               })

                            search_ids.append(result.id)

                view = self.env.ref(
                    'sh_bus_backend.sh_bus_search_result_tree_view')
                return {
                    'name': _('Search Result'),
                    'type': 'ir.actions.act_window',
                    "res_model": "sh.bus.search.result",
                    'views': [(view.id, 'tree')],
                    'view_mode': 'tree',
                    "target": "current",
                    "domain": [('id', 'in', search_ids)]
                }
