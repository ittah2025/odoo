# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.addons.sms_notification.models.messaging import send_message_sms

class PaymentLinkWizard(models.TransientModel):
    _inherit = "payment.link.wizard"
    _description = "Generate Payment Link"

    def send_the_link_by_sms(self):
        self.ensure_one()
        sms_body = self.link
        mobile_number = self.partner_id.phone
        gateway_id = self.env["sms.mail.server"].search([], order='sequence asc', limit=1)
        send_message_sms(self, self.partner_id, 'payment_link_generated')
        return {'type': 'ir.actions.act_window_close'}
