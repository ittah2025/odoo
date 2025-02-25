from odoo import models, api, fields, _
from .store_invoice_salla import SallaInvoice
from .store_customer_salla import respartner
from .store_product_salla import ProductTemplateOdooSalla
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime, timedelta
_logger = logging.getLogger(__name__)


class store_dashboard(models.Model):
    _name = 'store_dashboard'
    _description = 'Dashboard Kanban'

    name = fields.Char("Name")

    # def create_inv(self):
    #     AccountMove.create_saleorder(self)
    #     return 
    # def create_warehouse(self):
    #     Stockwarehouses.create_warehouse(self)
    #     return 
    # def create_reps(self):
    #     Reps.create_reps(self)
    #     return 
    # def create_product(self):
    #     product.create_product(self)
    #     return 
    def create_customer(self):
        counter = respartner.create_customer(self)
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = "{} Customer(s) imported from Salla Successfully".format(counter)
        return {
            'name': 'Success',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }
        return 

    def create_invoice(self):
        counter = SallaInvoice.create_invoice(self)
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = "{} Invoice(s) imported from Salla Successfully".format(counter)
        return {
            'name': 'Success',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }
        return 

    # def create_saleorder(self):
    #     super(salla_dashboard, self).create_saleorder()

    # def create_uomcateg(self):
    #     super(salla_dashboard, self).create_uomcateg()

    # def create_reps(self):
    #     super(salla_dashboard, self).create_reps()

    def create_product(self):
        ProductTemplateOdooSalla.create_product(self)
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = "Imported Products from Salla Successfully"
        return {
            'name': 'Success',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }
        return

    # def create_customer(self):
    #     super(store_dashboard, self).create_customer()

    # def action_view_customers(self):
    #     id="It works??"
    #     raise ValidationError(
    #         ("{}").format(id))

    # def create_category(self):
    #     super(salla_dashboard, self).create_category()
