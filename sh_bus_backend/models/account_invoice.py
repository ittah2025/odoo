# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class Payment(models.Model):
    _inherit = 'account.payment'

    def action_post(self):
        res = super(Payment, self).action_post()
        for rec in self:
            if rec.move_id and rec.move_id.ref:
                so_obj = self.env['sale.order'].sudo().search(
                    [('name', '=', rec.move_id.ref)])
                if so_obj and so_obj.trip_id:
                    for line in so_obj.order_line:
                        line.write({'booking_status': 'confirm'})
                        if line.seat:
                            self.env['bus.booked.seat'].sudo().create({'bus_id': so_obj.trip_id.id,
                                                                       'name': line.seat,
                                                                       'seat_id': line.seat_id
                                                                       })
        return res


class Move(models.Model):
    _inherit = 'account.move'

    trip_id = fields.Many2one('sh.bus.trip', string="Trip")


class InvoiceLine(models.Model):
    _inherit = 'account.move.line'

    seat = fields.Char("Seat Number")
    seat_id = fields.Char("Seat ID")
    p_name = fields.Char("Passenger Name")
    p_email = fields.Char("Email")
    p_age = fields.Char("Age")
    p_gender = fields.Char("Gender")
