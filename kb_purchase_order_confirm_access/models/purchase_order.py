from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        if not self.user_has_groups('kb_purchase_order_confirm_access.purchase_access_confirm_group'):
            raise ValidationError('You dont have access to confirm please contact your administrator')
        else:
            return super(PurchaseOrder, self).button_confirm()
