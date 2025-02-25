from odoo import api, fields, models, _
from datetime import date
from email.policy import default
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import datetime as dt
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class contract(models.Model):
    _name = "contract"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    customer_id = fields.Many2one('res.partner', 'Tenant Data')
    contract_sellingDate = fields.Date(string='Contract Selling Date')
    period_of_contract = fields.Selection([('1month', '1 Month'), ('3months', '3 Months'), ('4months', '4 Months'), ('6months', '6 Months')], string='Period Of contract')
    Tenancy_startDate = fields.Date(string='Tenancy Start Date')
    Tenancy_endDate = fields.Date(string='Tenancy End Date')
    transportation = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Transportation" , default="no" )

    transportation_period = fields.Selection([
        ('1month_450', '1 Month 450SR'),
        ('3months_1350', '3 Months 1350SR'),
        ('4months_1800', '4 Months 1800SR'),
        ('6months_2700', '6 Months 2700SR'),
    ], string='Period of Transportation')

    apartment_ids = fields.Many2one('apartments', string="Apartments")
    room_ids = fields.Many2one('rooms', string="Room")
    room_rent = fields.Boolean(string="Rented" ,related="room_ids.rented_room", readonly= False)
    

    contract_id = fields.Char(string='Contract No ', required=True,
                            copy=False, readonly=True, default=lambda self: _('New'))
    note = fields.Char()

    
    property_line_ids = fields.One2many('property.lines.ids', 'property_id',
                                            string='Payments Lines'
                                            )

    regRent_payment = fields.Float(string="Rent Payment")
    rent_payments = fields.Float(string="Number of Rent Payments")
    room_cost = fields.Float(string="Room Cost", related='room_ids.cost')
    apartment_cost = fields.Float(string="Apartment Cost", related='apartment_ids.final_total_apartment')
    total_contract_value = fields.Float(string="Total Contract Value") 
  

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Contract'
        if vals.get('contract_id', ('New')) == ('New'):
            vals['contract_id'] = self.env['ir.sequence'].next_by_code(
                'contract.seq') or ('New')
        res = super(contract, self).create(vals)
        return res


    def action_share_whatsapp(self):
        if not self.customer_id.phone:
            raise ValidationError(_("Missing phone number"))
        message = 'Hi %s, Your Contract Number is: %s , Will End This Month... Thank You' % (self.customer_id.name,self.contract_id) 
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.customer_id.phone,message)
        return {
            'type':'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url
        }

    #todo: cycle should be automatic

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_state(self):
        self.state = 'state'
        
    def action_new(self):
        self.state = 'new'

    state = fields.Selection([
        ('new', 'New'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
        ('state', 'State')
    ], readonly=True, default="new", help='Choose the state')

    # Room name is related to apartment
    @api.onchange('apartment_ids')
    def onchange_apartment(self):
        for rec in self:  
            return {'domain': {'room_ids': [('aprtment_id','=',rec.apartment_ids.id),('rented_room','=',False)]}}
            
    # @api.onchange('period_of_contract')
    def calculate(self):
        commands = []
        val = 0
        if self.id:
            commands.append((5, self.id))

        for rec in self: 
            if rec.transportation_period == '1month_450':
                val = 450
            elif rec.transportation_period == '3months_1350':
                val = 1350
            elif  rec.transportation_period == '4months_1800':
               val = 1800
            elif  rec.transportation_period == '6months_2700':
                val = 2700
            else:
                val = 0
            if rec.period_of_contract =='1month':
                rec.total_contract_value = rec.room_cost + val
            elif rec.period_of_contract =='3months':
                rec.total_contract_value = (rec.room_cost * 3) + val 
            elif  rec.period_of_contract =='4months':
                rec.total_contract_value = (rec.room_cost * 4) + val
            elif  rec.period_of_contract =='6months':
                rec.total_contract_value = (rec.room_cost * 6) + val 

            if rec.rent_payments:
                rec.regRent_payment = rec.total_contract_value / rec.rent_payments
                cycle = int(self.rent_payments)
                for i in range(cycle):
                    vals = {
                            'no': i+1,
                            'property_id': self.id,
                            'total': self.regRent_payment,
                            'payment_date': self.Tenancy_startDate
                        }
                    commands.append((0, False, vals))
            

                self.write({'property_line_ids': commands})
                return True



    def create_invoice(self):
        account_inv_obj = self.env['account.move']
        product_obj = self.env['product.product'].search([('name','=',self.room_ids.name)])
        # product_id = self.propertyId
        property_id = self.env['apartments'].search([], limit=1)
        vals  = {
            'move_type': 'out_invoice',
            'invoice_origin':self.id,
            'partner_id': self.customer_id.id,
            'invoice_user_id':1,
            'invoice_date': self.Tenancy_startDate,
            'invoice_line_ids': [(0,0,{
                'name': self.id,
                'product_id': product_obj.id,
                'price_unit': self.regRent_payment})],
        }
        invoice_id = account_inv_obj.create(vals)
        # raise ValidationError(_("{}".format(invoice_id)))
        if invoice_id:
            self.write({'id':invoice_id.id})
        else:
            raise ValidationError(_("Something went wrong"))
        self.action_confirm()
        return {
            'name': 'Partial Payment Invoice',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_id':invoice_id.id,
            'views': [(self.env.ref('account.view_move_form').id, 'form')],
            'res_model': 'account.move',
            'domain': [('id','=',invoice_id.id)],
        }



class property_lines_ids(models.Model):
    _name = "property.lines.ids"

    no = fields.Char(string="No.", readonly=True)
    total = fields.Float(string='Total', readonly=True)
    property_id = fields.Many2one('contract', readonly=True)
    payment_date = fields.Date(readonly=True)
    isPaid = fields.Boolean(string='Paid?', readonly= False, default= False)
    date_of_paid = fields.Date(string="Date of Paid")
    oneTimeEdit = fields.Boolean(compute="compute_date_of_paid_")
    

# define boolean field, Date of Paid (can't change after put it)
    def compute_date_of_paid_(self):
        for rec in self:
            rec.oneTimeEdit = False
            if rec.date_of_paid:
                rec.oneTimeEdit = True