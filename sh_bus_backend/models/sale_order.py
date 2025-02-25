# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class Contact(models.Model):
    _inherit = 'res.partner'

    type = fields.Selection(selection_add=[('passenger', 'Passenger')])


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_journal(self):
        return self.env['account.journal'].sudo().search([('type', '=', 'cash')], limit=1).id

    trip_id = fields.Many2one('sh.bus.trip', string="Trip")
    sale_paid = fields.Boolean('Sale Paid', default=False)
    paid_amount = fields.Float("Paid Amount")
    journal_id = fields.Many2one(
        'account.journal', string="Payment Method", default=_get_journal)
    date_travel = fields.Date("Journey Date", related='trip_id.trip_date')

    bording_from = fields.Many2one(
        'sh.bus.point', string="From", compute='get_so_data')
    to = fields.Many2one('sh.bus.point', string="To", compute='get_so_data')
    boarding_point = fields.Many2one(
        'sh.location.point', string="Boarding Point", compute='get_so_data')
    dropping_point = fields.Many2one(
        'sh.location.point', string="Dropping Point", compute='get_so_data')
    departure_time = fields.Char("Departure Time", compute='get_so_data')
    arrival_time = fields.Char("Arrival Time", compute='get_so_data')

    @api.depends('order_line.bording_from', 'order_line.to', 'order_line.trip_start_date', 'order_line.trip_end_date', 'order_line.departure_time', 'order_line.arrival_time')
    def get_so_data(self):
        for rec in self:
            rec.bording_from = False
            rec.to = False
            rec.boarding_point = False
            rec.dropping_point = False
            rec.departure_time = ''
            rec.arrival_time = ''

            if rec.order_line:
                count = 1
                for line in rec.order_line.filtered(lambda x: x.bording_from != False):
                    if count == 1:
                        rec.bording_from = line.bording_from.id
                        rec.to = line.to.id
                        rec.boarding_point = line.boarding_point.id
                        rec.dropping_point = line.dropping_point.id
                        rec.departure_time = line.departure_time
                        rec.arrival_time = line.arrival_time
                        count = 0

    @api.onchange('amount_total')
    def _onchange_total(self):
        if self.amount_total:
            self.paid_amount = self.amount_total

    def action_paid(self):
        for rec in self:
            rec.action_confirm()
            ctx = {'active_ids': [rec.id]}
            payment = self.env['sale.advance.payment.inv'].with_context(ctx).create({
                'fixed_amount': rec.amount_total,
            })
            payment.create_invoices()
            if rec.invoice_ids:
                for invoice in rec.invoice_ids:
                    if invoice:
                        invoice.action_post()
                        cash_journal = self.journal_id.id
                        payment_method_id = self.env['account.payment.method'].sudo().search(
                            [('payment_type', '=', 'inbound')], limit=1).id

                        payment_values = {'payment_type': 'inbound',
                                          'partner_id': rec.partner_id.id,
                                          'partner_type': 'customer',
                                          'journal_id': cash_journal,
                                          'company_id': rec.company_id.id,
                                          'currency_id': rec.pricelist_id.currency_id.id,
                                          'date': rec.date_order,
                                          'amount': rec.amount_total,
                                          'ref': rec.name,
                                          'reconciled_invoice_ids': [(6, 0, [invoice.id])],
                                          'payment_method_id': payment_method_id
                                          }
                        payment = self.env['account.payment'].create(
                            payment_values)
                        payment.action_post()
                        if payment.move_id:
                            for line in payment.move_id.line_ids.filtered(lambda x: x.account_internal_type in ('receivable', 'payable') and not x.reconciled):
                                payment_lines = line

                        if invoice.line_ids:
                            for line in invoice.line_ids.filtered(lambda x: x.account_internal_type in ('receivable', 'payable') and not x.reconciled):
                                payment_lines += line

                        payment_lines.reconcile()
                        rec.write({'sale_paid': True})

                        for line in rec.order_line:
                            line.write({'booking_status': 'confirm'})

    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()

        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        if self.trip_id:
            invoice_vals.update({'trip_id': self.trip_id.id})
        return invoice_vals


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    seat = fields.Char("Seat Number")
    seat_id = fields.Char("Seat ID")
    p_name = fields.Char("Passenger Name")
    p_email = fields.Char("Email")
    p_age = fields.Char("Age")
    p_gender = fields.Char("Gender")
    boarding_point = fields.Many2one(
        'sh.location.point', string="Boarding Point")
    dropping_point = fields.Many2one(
        'sh.location.point', string="Dropping Point")

    trip_id = fields.Many2one('sh.bus.trip', string="Trip")
    search_id = fields.Many2one(
        'sh.bus.search.result', string="Search Result Id")
    bording_from = fields.Many2one(
        'sh.bus.point', string="From", related='search_id.bording_from')
    to = fields.Many2one('sh.bus.point', string="To", related='search_id.to')
    trip_start_date = fields.Float(
        string="Start Time", related='search_id.trip_start_date')
    trip_end_date = fields.Float(
        string="Stop Time", related='search_id.trip_end_date')
    booking_status = fields.Selection([('draft', 'Not Confirmed'),
                                       ('confirm', 'Confirmed'),
                                       ('cancel', 'Cancel'),
                                       ('check_in', 'Check in')], default='draft')

    departure_time = fields.Char(
        "Departure Time", compute='get_departure_time')
    arrival_time = fields.Char("Arrival Time", compute='get_arrival_time')

    @api.depends('trip_start_date')
    def get_departure_time(self):
        for rec in self:
            rec.departure_time = ''
            if rec.trip_start_date:
                if rec.trip_start_date < 13.0:
                    rec.departure_time = '{0:02.0f}:{1:02.0f}'.format(
                        *divmod(rec.trip_start_date * 60, 60)) + ' AM'
                else:
                    time = rec.trip_start_date - 12.0
                    rec.departure_time = '{0:02.0f}:{1:02.0f}'.format(
                        *divmod(time * 60, 60)) + ' PM'

    @api.depends('trip_end_date')
    def get_arrival_time(self):
        for rec in self:
            rec.arrival_time = ''
            if rec.trip_end_date:
                if rec.trip_end_date < 13.0:
                    rec.arrival_time = '{0:02.0f}:{1:02.0f}'.format(
                        *divmod(rec.trip_end_date * 60, 60)) + ' AM'
                else:
                    time = rec.trip_end_date - 12.0
                    rec.arrival_time = '{0:02.0f}:{1:02.0f}'.format(
                        *divmod(time * 60, 60)) + ' PM'

    def action_check_seat(self):
        for rec in self:
            rec.write({'booking_status': 'check_in'})

    def action_cancel_seat(self):
        for rec in self:
            if rec.trip_id:
                booked_seat_id = self.env['bus.booked.seat'].sudo().search(
                    [('bus_id', '=', rec.trip_id.id), ('seat_id', '=', rec.seat_id)])
                if booked_seat_id:
                    booked_seat_id.unlink()
            rec.write({'booking_status': 'cancel'})

    def _prepare_invoice_line(self, **optional_values):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()

        res = super(SaleOrderLine, self)._prepare_invoice_line()
        if self.seat and self.p_name:
            res.update({
                'seat': self.seat,
                'seat_id': self.seat_id,
                'p_name': self.p_name,
                'p_email': self.p_email,
                'p_age': self.p_age,
                'p_gender': self.p_gender,

            })

        return res
