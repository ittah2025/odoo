# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import json
import binascii
from datetime import date
from odoo import fields, http
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.osv import expression
from odoo import _
from odoo.http import request
from datetime import datetime
from odoo.tools.safe_eval import safe_eval
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.portal.controllers.portal import get_records_pager
from odoo.addons.sale.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):
    
    @http.route(['/my/orders/<int:order_id>'], type='http', auth="public", website=True)
    def portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            
             # -------- Softhealer
            return self._show_report(model=order_sudo, report_type=report_type, report_ref='sh_bus_backend.ticket_report', download=download)
            # -------- Softhealer
            
#             return self._show_report(model=order_sudo, report_type=report_type, report_ref='sale.action_report_saleorder', download=download)

        # use sudo to allow accessing/viewing orders for public user
        # only if he knows the private token
        # Log only once a day
        if order_sudo:
            # store the date as a string in the session to allow serialization
            now = fields.Date.today().isoformat()
            session_obj_date = request.session.get('view_quote_%s' % order_sudo.id)
            if session_obj_date != now and request.env.user.share and access_token:
                request.session['view_quote_%s' % order_sudo.id] = now
                body = _('Quotation viewed by customer %s', order_sudo.partner_id.name)
                _message_post_helper(
                    "sale.order",
                    order_sudo.id,
                    body,
                    token=order_sudo.access_token,
                    message_type="notification",
                    subtype_xmlid="mail.mt_note",
                    partner_ids=order_sudo.user_id.sudo().partner_id.ids,
                )

        values = {
            'sale_order': order_sudo,
            'message': message,
            'token': access_token,
            'landing_route': '/shop/payment/validate',
            'bootstrap_formatting': True,
            'partner_id': order_sudo.partner_id.id,
            'report_type': 'html',
            'action': order_sudo._get_portal_return_action(),
        }
        if order_sudo.company_id:
            values['res_company'] = order_sudo.company_id

        # Payment values
        if order_sudo.has_to_be_paid():
            logged_in = not request.env.user._is_public()
            acquirers_sudo = request.env['payment.acquirer'].sudo()._get_compatible_acquirers(
                order_sudo.company_id.id,
                order_sudo.partner_id.id,
                currency_id=order_sudo.currency_id.id,
                sale_order_id=order_sudo.id,
            )  # In sudo mode to read the fields of acquirers and partner (if not logged in)
            tokens = request.env['payment.token'].search([
                ('acquirer_id', 'in', acquirers_sudo.ids),
                ('partner_id', '=', order_sudo.partner_id.id)
            ]) if logged_in else request.env['payment.token']
            fees_by_acquirer = {
                acquirer: acquirer._compute_fees(
                    order_sudo.amount_total,
                    order_sudo.currency_id,
                    order_sudo.partner_id.country_id,
                ) for acquirer in acquirers_sudo.filtered('fees_active')
            }
            # Prevent public partner from saving payment methods but force it for logged in partners
            # buying subscription products
            show_tokenize_input = logged_in \
                and not request.env['payment.acquirer'].sudo()._is_tokenization_required(
                    sale_order_id=order_sudo.id
                )
            values.update({
                'acquirers': acquirers_sudo,
                'tokens': tokens,
                'fees_by_acquirer': fees_by_acquirer,
                'show_tokenize_input': show_tokenize_input,
                'amount': order_sudo.amount_total,
                'currency': order_sudo.pricelist_id.currency_id,
                'partner_id': order_sudo.partner_id.id,
                'access_token': order_sudo.access_token,
                'transaction_route': order_sudo.get_portal_url(suffix='/transaction'),
                'landing_route': order_sudo.get_portal_url(),
            })

        if order_sudo.state in ('draft', 'sent', 'cancel'):
            history = request.session.get('my_quotations_history', [])
        else:
            history = request.session.get('my_orders_history', [])
        values.update(get_records_pager(history, order_sudo))

        return request.render('sale.sale_order_portal_template', values)


    @http.route(['/my/orders/<int:order_id>/accept'], type='json', auth="public", website=True)
    def portal_quote_accept(self, order_id, access_token=None, name=None, signature=None):
        # get from query string if not on json param
        access_token = access_token or request.httprequest.args.get(
            'access_token')
        try:
            order_sudo = self._document_check_access(
                'sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return {'error': _('Invalid order.')}

        if not order_sudo.has_to_be_signed():
            return {'error': _('The order is not in a state requiring customer signature.')}
        if not signature:
            return {'error': _('Signature is missing.')}

        try:
            order_sudo.write({
                'signed_by': name,
                'signed_on': fields.Datetime.now(),
                'signature': signature,
            })
            request.env.cr.commit()
        except (TypeError, binascii.Error) as e:
            return {'error': _('Invalid signature data.')}

        if not order_sudo.has_to_be_paid():
            order_sudo.action_confirm()
            order_sudo._send_order_confirmation_mail()

        # -------- Softhealer
        pdf = request.env.ref('sh_bus_backend.ticket_report').sudo(
        ).render_qweb_pdf([order_sudo.id])[0]
        # -------- Softhealer
        _message_post_helper(
            'sale.order', order_sudo.id, _('Order signed by %s') % (name,),
            attachments=[('%s.pdf' % order_sudo.name, pdf)],
            **({'token': access_token} if access_token else {}))

        query_string = '&message=sign_ok'
        if order_sudo.has_to_be_paid(True):
            query_string += '#allow_payment=yes'
        return {
            'force_refresh': True,
            'redirect_url': order_sudo.get_portal_url(query_string=query_string),
        }


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/print'], type='http', auth="public", website=True, sitemap=False)
    def print_saleorder(self, **kwargs):
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            pdf, _ = request.env.ref('sh_bus_backend.ticket_report').sudo(
            )._render_qweb_pdf([sale_order_id])
            pdfhttpheaders = [('Content-Type', 'application/pdf'),
                              ('Content-Length', u'%s' % len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            return request.redirect('/shop')

    @http.route(['/shop/confirm_order'], type='http', auth="public", website=True, sitemap=False)
    def confirm_order(self, **post):
        order = request.website.sale_get_order()

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        order.onchange_partner_shipping_id()
        order.order_line._compute_tax_id()
        request.session['sale_last_order_id'] = order.id
        # -------- Softhealer
        # request.website.sale_get_order(update_pricelist=True)
        # -------- Softhealer
        extra_step = request.website.viewref('website_sale.extra_info_option')
        if extra_step.active:
            return request.redirect("/shop/extra_info")

        return request.redirect("/shop/payment")


class WebsiteScore(http.Controller):

    @http.route(['''/add_cart_ticket'''], type='http', auth="public", website=True, csrf=False)
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
                        [('default_code', '=', 'ticket'), ('is_published', '=', True)], limit=1)
                    if not product:
                        product = request.env['product.product'].sudo().create({'default_code': 'ticket',
                                                                                'name': 'Bus Ticket',
                                                                                'type': 'service',
                                                                                'is_published': True
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
                            [('default_code', '=', 'ticket'), ('is_published', '=', True)], limit=1)
                        if not product:
                            product = request.env['product.product'].sudo().create({'default_code': 'ticket',
                                                                                    'name': 'Bus Ticket',
                                                                                    'type': 'service',
                                                                                    'is_published': True
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

                        # other contact as partner
                        request.env['res.partner'].sudo().create({
                            'type': 'passenger',
                            'parent_id': partner.id,
                            'name': str(passenger[3]),
                            'email': str(passenger[4]),
                        })

                        request.env['sale.order.line'].sudo().create(
                            order_line_vals)

        base_url = request.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
        request.session['sale_order_id'] = sale_order.id

        bigData = {
            'id': sale_order.id,
            'base_url': base_url
        }
        return json.dumps(bigData)

    @http.route(['''/get_booked_seat'''], type='http', auth="public", website=True, csrf=False)
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
#
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

    def serach_bus_frontend(self, from_location, to_location, date, fleet_type):
        if date and from_location and to_location:
            # date = datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")
            date = date
            domain = [('bording_from', '=', from_location)]

            if fleet_type:
                domain.append(
                    ('route_line.fleet_id.fleet_type', '=', int(fleet_type)))

            route_line_from = request.env['sh.route.line'].sudo().search(
                domain)
            # first check from location
            search_ids = []
            if route_line_from:
                for each_line in route_line_from:
                    rid = each_line.route_line.id
                    fleet_id = each_line.route_line.fleet_id.id
                    # get route id and check to location with higher id of that route line
                    route_line_to = request.env['sh.route.line'].sudo().search(
                        [('route_line', '=', rid), ('id', '>=', each_line.id), ('to', '=', to_location)])

                    if route_line_to:
                        # Bus is available
                        # check in bus trip
                        existing_trip = request.env['sh.bus.trip'].sudo().search([('route', '=', rid), ('trip_date', '=', date),
                                                                                  ('bus_id', '=', fleet_id)], limit=1)

                        if not existing_trip:
                            existing_trip = request.env['sh.bus.trip'].sudo().create({
                                'route': rid,
                                'trip_date': date,
                                'bus_id': fleet_id,

                            })

                        # check in bus search result
                        trips = request.env['sh.bus.search.result'].sudo().search([('route', '=', rid), ('trip_date', '=', date),
                                                                                   ('bus_id', '=',
                                                                                    fleet_id),
                                                                                   ('bording_from',
                                                                                    '=', from_location),
                                                                                   ('to', '=', to_location)])
                        if trips:
                            for trip in trips:
                                search_ids.append(trip)
                                if existing_trip.booked_seat_ids:
                                    for booked_seat_id in existing_trip.booked_seat_ids:
                                        search_bus_id = request.env['bus.booked.seat'].sudo().create({'search_id': trip.id,
                                                                                                      'name': booked_seat_id.name,
                                                                                                      'seat_id': booked_seat_id.seat_id
                                                                                                      })

                        else:
                            from_location_obj = request.env['sh.bus.point'].sudo().browse(
                                from_location)
                            to_location_obj = request.env['sh.bus.point'].sudo().browse(
                                to_location)
                            result = request.env['sh.bus.search.result'].sudo().create({
                                'route': rid,
                                'trip_date': date,
                                'trip_start_date': each_line.start_times,
                                'trip_end_date': route_line_to.end_times,
                                'bus_id': fleet_id,
                                'price': each_line.route_line.get_price(from_location_obj, to_location_obj),
                                'bording_from': from_location,
                                'to': to_location,
                                'trip_id': existing_trip.id
                            })
                            if existing_trip.booked_seat_ids:
                                for booked_seat_id in existing_trip.booked_seat_ids:
                                    search_bus_id = request.env['bus.booked.seat'].sudo().create({'search_id': result.id,
                                                                                                  'name': booked_seat_id.name,
                                                                                                  'seat_id': booked_seat_id.seat_id
                                                                                                  })

                            search_ids.append(result)

                return search_ids

    @http.route(['''/busBooking'''], type='http', auth="public", website=True)
    def EventSeatBooking(self, **kwargs):
        points = []
        for point in request.env['sh.bus.point'].sudo().search([]):
            points.append(point)

        bus_types = []
        for bus_type in request.env['sh.bus.type'].sudo().search([]):
            bus_types.append(bus_type)
        if kwargs:
            search_ids = []

            if kwargs.get('start_point', False) and kwargs.get('end_point', False) and kwargs.get('date', False):
                fleet_type = False

                search_date = ''
                if kwargs.get('fleet_type'):
                    fleet_type = kwargs.get('fleet_type')

                search_ids = self.serach_bus_frontend(int(kwargs.get('start_point')), int(
                    kwargs.get('end_point')), kwargs.get('date'), fleet_type)

                search_date = kwargs.get('date')
            return request.render("sh_bus_frontend.website_bus_booking_template", {'points': points, 'to_points': points, 'bus_types': bus_types, 'main_form': False, 'search_ids': search_ids, 'from_loc': kwargs.get('start_point', False), 'to_loc': kwargs.get('end_point', False), 'fleet_type': kwargs.get('fleet_type', False), 'search_date': search_date})

        return request.render("sh_bus_frontend.website_bus_booking_template", {'points': points, 'bus_types': bus_types, 'main_form': True})
