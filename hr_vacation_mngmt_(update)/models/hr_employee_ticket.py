# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.exceptions import UserError

class HrFlightTicket(models.Model):
    _name = 'hr.flight.ticket'

    name = fields.Char()
    employee_id = fields.Many2one('hr.leave', string='Employee', required=True, help="Employee" )
    ticket_type = fields.Selection([('one', 'One Way'), ('round', 'Round Trip')], string='Ticket Type', default='round', help="Select the ticket type")
    depart_from = fields.Char(string='Departure', help="Departure")
    destination = fields.Char(string='Destination', help="Destination")
    date_start = fields.Datetime(string='Start Date', help="Start date")
    date_return = fields.Datetime(string='Return Date', help="Return date")
    ticket_class = fields.Selection([('economy', 'Economy'),
                                     ('premium_economy', 'Premium Economy'),
                                     ('business', 'Business'),
                                     ('first_class', 'First Class')], string='Class', help="Select the ticket class")
    ticket_fare = fields.Float(string='Ticket Fare', help="Give the ticket fare")
    flight_details = fields.Text(string='Flight Details', help="Flight details")
    return_flight_details = fields.Text(string='Return Flight Details', help="return flight details")
    country_ = fields.Many2one('res.country', string='Country')
    ticket_fare_on = fields.Selection([('company', 'Company'),
                                     ('employee', 'Employee'),
                                     ], string='Ticket Fare On Account', required=True, help="Select the ticket Account")

    state = fields.Selection([('booked', 'Booked'), ('confirmed', 'Confirmed'), ('started', 'Started'),
                              ('completed', 'Completed'), ('canceled', 'Canceled')], string='Status', default='booked')
    invoice_id = fields.Many2one('account.move', string='Invoice', help="Invoice")
    leave_id = fields.Many2one('hr.leave', string='Leave', help="Leave")
    company_id = fields.Many2one('res.company', 'Company', help="Company", default=lambda self: self.env.user.company_id)
    is_ticket = fields.Boolean(default=False , string='Ticket Fare On Company')

    def name_get(self):
        res = []
        for ticket in self:
            res.append((ticket.id, _("Flight ticket for %s on %s to %s") % (
                ticket.employee_id.name, ticket.date_start, ticket.destination)))
        return res

    @api.constrains('date_start', 'date_return')
    def check_valid_date(self):
        if self.filtered(lambda c: c.date_return and c.date_start > c.date_return):
            raise ValidationError(_('Flight travelling start date must be less than flight return date.'))

    def book_ticket(self):
        return {'type': 'ir.actions.act_window_close'}

    def confirm_ticket(self):
        product_id = self.env['product.product'].search([("name", "=", "Flight Ticket")])
        if self.ticket_fare <= 0:
            raise UserError(_('Please add ticket fare.'))
        inv_obj = self.env['account.move']
        expense_account = self.env['ir.config_parameter'].sudo().get_param('travel_expense_account')
        if not expense_account:
            raise UserError(_('Please select expense account for the flight tickets.'))
        domain = [
            ('type', '=', 'purchase'),
            ('company_id', '=', self.company_id.id),
        ]
        journal_id = self.env['account.journal'].search(domain, limit=1)
        partner = self.env.ref('hr_vacation_mngmt.air_lines_partner')
        if not partner.property_payment_term_id:
            date_due = fields.Date.context_today(self)
        else:
            pterm = partner.property_payment_term_id
            pterm_list = \
                pterm.with_context(currency_id=self.env.user.company_id.id).compute(
                    value=1, date_ref=fields.Date.context_today(self))[0]
            date_due = max(line[0] for line in pterm_list)
        inv_id = self.env['account.move'].create({
            'name': '/',
            'invoice_origin': 'Flight Ticket',
            'move_type': 'in_invoice',
            'journal_id': journal_id.id,
            # 'invoice_payment_term_id': partner.property_payment_term_id.id,
            'invoice_date_due': date_due,
            'ref': False,
            'partner_id': partner.id,
            # 'invoice_partner_bank_id': partner.property_account_payable_id.id,
            'state': 'draft',
            'invoice_line_ids': [(0, 0, {
                'name': 'Flight Ticket',
                'price_unit': self.ticket_fare,
                'quantity': 1.0,
                'account_id': int(expense_account),
                'product_id': product_id.id,
            })],
        })
        # inv_id.action_invoice_open()
        self.write({'state': 'confirmed', 'invoice_id': inv_id.id})

    def cancel_ticket(self):
        if self.state == 'booked':
            self.write({'state': 'canceled'})
        elif self.state == 'confirmed':
            if self.invoice_id and self.invoice_id.state == 'draft':
                self.write({'state': 'canceled'})
            if self.invoice_id and self.invoice_id.state == 'open':
                self.invoice_id.action_invoice_cancel()
                self.write({'state': 'canceled'})

    @api.model
    def run_update_ticket_status(self):
        run_out_tickets = self.search([('state', 'in', ['confirmed', 'started']),
                                       ('date_return', '<=', datetime.now())])
        confirmed_tickets = self.search([('state', '=', 'confirmed'), ('date_start', '<=', datetime.now()),
                                         ('date_return', '>', datetime.now())])
        for ticket in run_out_tickets:
            ticket.write({'state': 'completed'})
        for ticket in confirmed_tickets:
            ticket.write({'state': 'started'})

    def action_view_invoice(self):
        return {
            'name': _('Flight Ticket Invoice'),
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
            'res_model': 'account.move',
            'context': "{'type':'in_invoice'}",
            'type': 'ir.actions.act_window',
            'res_id': self.invoice_id.id,
        }

    @api.onchange('employee_id')
    def create_ticket(self):
        ticket_id = self.env['hr.contract'].search([], limit=1, order='id desc')
        for rec in self: 
            for record in ticket_id:
                for rec2 in self.employee_id:
                    if rec2.employee_ids == record.employee_id:
                        # raise ValidationError(_(record.date_end))
                        time_deffernce = relativedelta(record.date_end, record.date_start)
                        difference_in_years = time_deffernce.years
                        if difference_in_years == 2:
                            rec.ticket_fare_on = 'company'
                            self.is_ticket = True
                            # raise UserError("Contract duration 2 years, the ticket fare on company")
                        else:
                            rec.ticket_fare_on = 'employee'
                            self.is_ticket = False
                            # raise UserError("Contract is less than 2 years, the ticket fare on employee")
    
    @api.onchange('employee_id')
    def check_name(self):
        contract = self.env['extensionof.exit'].search([("name","=",self.employee_id.employee_ids.id)])
        cantoryeml = self.env['hr.employee'].search(['&',("name","=",self.employee_id.employee_ids.name),('country_id.id','=',192)])
        for rec in self:
            if rec.employee_id:
                if cantoryeml:
                    pass
                else:
                    if contract:
                        pass
                    else:
                        raise UserError("The employee don't have Extension of Exit and Return visa")           
                
   
