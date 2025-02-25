from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import datetime as dt
from datetime import datetime, timedelta
from datetime import date

class SummaryReportWizard(models.Model):
    _name = "summary_report_wizard"
    _table = "summary_report_wizard"
    _description = "Summary Report"


    apartment_ids = fields.Many2one('apartments', string="Apartments")
    customer_id = fields.Many2one('res.partner', 'Tenant Data')
    properyId = fields.Many2one('property', 'Room Name')

    date_froms = fields.Date(string="From Date")
    date_tos = fields.Date(string="To Date")

    date_from = fields.Date(string="From Date")
    date_to = fields.Date(string="To Date")
    summ = fields.Float()

# Print Late Payment
    def late_pay_(self):
        domain = []
        payment_list = []
        data = {
            'form_data': self.read()[0],
            'propertyids': payment_list
            }

        if data['form_data']['apartment_ids']:
           selected_property = data['form_data']['apartment_ids'][0]
        #    raise ValidationError(_("{}".format(selected_customer)))
           propertyids = self.env['contract'].search([('apartment_ids','=', selected_property)])
        else:
           propertyids = self.env['contract'].search([])
        for prop in propertyids:
            for propertyid in prop.property_line_ids:
                if (propertyid.isPaid == False):
                    vals = {
                    'apartment_ids': prop.apartment_ids.name,
                    'room_ids': prop.room_ids.name,
                    'customer_id': prop.customer_id.name,
                    'no': propertyid.no,
                    'total': propertyid.total,
                    'payment_date': propertyid.payment_date,
                    }
                    payment_list.append(vals)
        return self.env.ref('kb_property_managment_alsalem.action_late_payment_report').report_action(self, data=data)


# Print All Payment
    def all_pay_(self):
        domain = []
        payment_list = []
        data = {
            'form_data': self.read()[0],
            'propertyids': payment_list
            }

        if data['form_data']['apartment_ids']:
           selected_property = data['form_data']['apartment_ids'][0]
           propertyids = self.env['contract'].search([('apartment_ids','=', selected_property)])
        else:
           propertyids = self.env['contract'].search([])
        for prop2 in propertyids:
            for propertyid in prop2.property_line_ids:
                vals = {
                    'apartment_ids': prop2.apartment_ids.name,
                    'room_ids': prop2.room_ids.name,
                    'customer_id': prop2.customer_id.name,
                    'no': propertyid.no,
                    'total': propertyid.total,
                    'payment_date': propertyid.payment_date,
                    'date_of_paid': propertyid.date_of_paid,
                }
                payment_list.append(vals)
        return self.env.ref('kb_property_managment_alsalem.action_all_payment_report').report_action(self, data=data)

# print PDF
    def action_summary_print(self):
        domain = []
        propertyid_list = []
        data = {
            'form_data': self.read()[0],
            'propertyids': propertyid_list
            }

        if data['form_data']['customer_id']:
           selected_customer = data['form_data']['customer_id'][0]
           propertyids = self.env['contract'].search([('customer_id','=', selected_customer)])
        else:
           propertyids = self.env['contract'].search([])

        for propertyid in propertyids:
            vals = {
                'customer_id': propertyid.customer_id.name,
                # 'contract_sellingDate': propertyid.contract_sellingDate,
                'contract_id': propertyid.contract_id,
                'Tenancy_startDate': propertyid.Tenancy_startDate,
                'Tenancy_endDate': propertyid.Tenancy_endDate,
                'regRent_payment': propertyid.regRent_payment,
                'rent_payments': propertyid.rent_payments,
                'room_cost': propertyid.room_cost,
                'total_contract_value': propertyid.total_contract_value,
               
            }
            propertyid_list.append(vals)
        return self.env.ref('kb_property_managment_alsalem.action_summary_report').report_action(self, data=data)

# Profit Report
    def summary_profit_report(self):
        domain = []
        contId_list = []
        data = {
            'form_data': self.read()[0],
            'contId': contId_list
            }

        if data['form_data']['apartment_ids']:
           selected_apart = data['form_data']['apartment_ids'][0]
           contId = self.env['contract'].search([('apartment_ids','=', selected_apart)])
        else:
            contId = self.env['contract'].search([])

        # self.summ = 0

        # for contt in contId:
        #     self.summ += contt.room_cost
        # raise ValidationError(_(self.summ))
            
        for cont in contId:
            vals = {
                'apartment_ids': cont.apartment_ids.name,
                'room_ids': cont.room_ids.name,
                'room_cost': cont.room_cost,
            }
            contId_list.append(vals)
        return self.env.ref('kb_property_managment_alsalem.action_profite_report').report_action(self, data=data)
