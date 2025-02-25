# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import json
from odoo import http
from odoo.http import request
from odoo.tools.safe_eval import safe_eval


class Website(http.Controller):

    @http.route(['''/next_checkout'''], type='http', auth="public", website=True, csrf=False)
    def next_checkout(self, **post):

        trip_id = False
        if post.get('search_trip_id'):
            search_id = request.env['sh.bus.search.result'].sudo().browse(
                int(post.get('search_trip_id')))
            if search_id and search_id.trip_id:
                trip_id = search_id.trip_id.id

        if post.get('data_list'):

            passenger_detail = post.get('data_list')
            count = 0
            sale_order = False
            for passenger in safe_eval(passenger_detail):
                if count == 0:

                    partner = request.env['res.partner'].sudo().search(
                        [('email', '=', str(passenger[4]))], limit=1)
                    if not partner:
                        partner = request.env['res.partner'].sudo().create({'name': str(passenger[3]),
                                                                            'email': str(passenger[4]),
                                                                            'type': 'passenger',
                                                                            })

                    sale_order = request.env['sale.order'].sudo().create(
                        {'partner_id': partner.id, 'trip_id': trip_id})

                    product = request.env['product.product'].sudo().search(
                        [('default_code', '=', 'ticket')], limit=1)
                    if not product:
                        product = request.env['product.product'].sudo().create({'default_code': 'ticket',
                                                                                'name': 'Bus Ticket',
                                                                                'type': 'service',
                                                                                })

                    order_line_vals = {'product_id': product.id,
                                       'name': product.name,
                                       'product_uom_qty': 1.0,
                                       'price_unit': float(passenger[2]),
                                       'order_id': sale_order.id,
                                       'seat': str(passenger[1]),
                                       'seat_id': str(passenger[0]),
                                       'p_name': str(passenger[3]),
                                       'p_email': str(passenger[4]),
                                       'p_age': str(passenger[5]),
                                       'p_gender': str(passenger[6]),
                                       'boarding_point': str(passenger[7]),
                                       'dropping_point': str(passenger[8]),
                                       'trip_id': trip_id,
                                       'search_id': search_id.id
                                       }
                    request.env['sale.order.line'].sudo().create(
                        order_line_vals)

                    count = 1
                else:
                    if sale_order:
                        product = request.env['product.product'].sudo().search(
                            [('default_code', '=', 'ticket')], limit=1)
                        if not product:
                            product = request.env['product.product'].sudo().create({'default_code': 'ticket',
                                                                                    'name': 'Bus Ticket',
                                                                                    'type': 'service',
                                                                                    })

                        order_line_vals = {'product_id': product.id,
                                           'name': product.name,
                                           'product_uom_qty': 1.0,
                                           'price_unit': float(passenger[2]),
                                           'order_id': sale_order.id,
                                           'seat': str(passenger[1]),
                                           'seat_id': str(passenger[0]),
                                           'p_name': str(passenger[3]),
                                           'p_email': str(passenger[4]),
                                           'p_age': str(passenger[5]),
                                           'p_gender': str(passenger[6]),
                                           'boarding_point': str(passenger[7]),
                                           'dropping_point': str(passenger[8]),
                                           'trip_id': trip_id,
                                           'search_id': search_id.id
                                           }

                        #other contact as partner
                        request.env['res.partner'].sudo().create({
                            'type': 'passenger',
                            'parent_id': partner.id,
                            'name': str(passenger[3]),
                            'email': str(passenger[4]),
                        })

                        request.env['sale.order.line'].sudo().create(
                            order_line_vals)


#
        base_url = request.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')

        bigData = {
            'id': sale_order.id,
            'base_url': base_url
        }
        return json.dumps(bigData)

    @http.route(['''/get_json_data_from_registration'''], type='http', auth="public", website=True, csrf=False)
    def get_json_data_from_registration(self, bus_type_id):
        bus_type_obj = request.env['sh.bus.type'].sudo().browse(
            int(bus_type_id))
        data = []
        seats = {}
        legend_items = []
        ticket_type_list = ['0', 'a', 'b', 'c', 'd', 'e',
                            'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']
        if bus_type_obj:
            max_cols = bus_type_obj.col_count
            i = 1

            seats[ticket_type_list[i]] = {
                'price': 0.0, 'classes': ticket_type_list[i]+'-class', 'category': 'Standard'}
            legend_items.append([ticket_type_list[i], 'available', 'Standard'])
            for row in range(bus_type_obj.row_count):
                if bus_type_obj.layout == '2-2':
                    seat_arrangement = 'aa_aa'
                    data.append(seat_arrangement)
                elif bus_type_obj.layout == '1-1':
                    seat_arrangement = 'a_a'
                    data.append(seat_arrangement)
                elif bus_type_obj.layout == '2-1':
                    seat_arrangement = 'aa_a'
                    data.append(seat_arrangement)
                elif bus_type_obj.layout == '1-2':
                    seat_arrangement = 'a_aa'
                    data.append(seat_arrangement)
                elif bus_type_obj.layout == '3-2':
                    seat_arrangement = 'aaa_aa'
                    data.append(seat_arrangement)
                elif bus_type_obj.layout == '2-3':
                    seat_arrangement = 'aa_aaa'
                    data.append(seat_arrangement)

        legend_items.append(['f', 'unavailable', 'Already Booked'])
        booked_seat_list = []
#         if event_id and event_id.booked_seat_ids:
#             for booked_seat in event_id.booked_seat_ids:
#                 booked_seat_list.append(booked_seat.name)
#
        bigData = {
            'data': data,
            'seats': seats,
            'legend_items': legend_items,
            'booked_seat': booked_seat_list,
        }

        return json.dumps(bigData)

    @http.route(['''/get_booked_seat_data'''], type='http', auth="public", website=True, csrf=False)
    def get_booked_seat_data(self, trip_id):
        trip_obj = request.env['sh.bus.search.result'].sudo().browse(
            int(trip_id))
        data = []
        seats = {}
        legend_items = []
        ticket_type_list = ['0', 'a', 'b', 'c', 'd', 'e',
                            'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']
        if trip_obj.bus_id and trip_obj.bus_id.fleet_type:
            bus_type_obj = trip_obj.bus_id.fleet_type
            price = trip_obj.price
            max_cols = bus_type_obj.col_count
            i = 1

            seats[ticket_type_list[i]] = {
                'price': price, 'classes': ticket_type_list[i]+'-class', 'category': 'Standard'}
            legend_items.append([ticket_type_list[i], 'available', 'Standard'])
            for row in range(bus_type_obj.row_count):
                if bus_type_obj.layout == '2-2':
                    seat_arrangement = 'aa_aa'
                    data.append(seat_arrangement)
                elif bus_type_obj.layout == '1-1':
                    seat_arrangement = 'a_a'
                    data.append(seat_arrangement)
                elif bus_type_obj.layout == '2-1':
                    seat_arrangement = 'aa_a'
                    data.append(seat_arrangement)
                elif bus_type_obj.layout == '1-2':
                    seat_arrangement = 'a_aa'
                    data.append(seat_arrangement)
                elif bus_type_obj.layout == '3-2':
                    seat_arrangement = 'aaa_aa'
                    data.append(seat_arrangement)
                elif bus_type_obj.layout == '2-3':
                    seat_arrangement = 'aa_aaa'
                    data.append(seat_arrangement)

        legend_items.append(['f', 'unavailable', 'Already Booked'])
        booked_seat_list = []
        if trip_obj and trip_obj.booked_seat_ids:
            for booked_seat in trip_obj.booked_seat_ids:
                booked_seat_list.append(booked_seat.seat_id)
#
        boarding_points = []
        dropping_points = []
        if trip_obj.bording_from and trip_obj.bording_from.point_ids:
            for point in trip_obj.bording_from.point_ids:
                boarding_points.append([point.id, point.name])
        if trip_obj.to and trip_obj.to.point_ids:
            for point in trip_obj.to.point_ids:
                dropping_points.append([point.id, point.name])

        amenities_list = []
        if trip_obj.bus_id.amenities_ids:
            for amenities in trip_obj.bus_id.amenities_ids:
                amenities_list.append([amenities.name])

        bigData = {
            'data': data,
            'seats': seats,
            'legend_items': legend_items,
            'booked_seat': booked_seat_list,
            'currency': request.env.user.company_id.currency_id.symbol,
            'boarding_points': boarding_points,
            'dropping_points': dropping_points,
            'amenities_list': amenities_list
        }
        return json.dumps(bigData)
