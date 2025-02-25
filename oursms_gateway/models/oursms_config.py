# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
##########################################################################

import logging
from odoo import models, fields, api, _
from .oursms_messaging import send_sms_using_oursms
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SmsMailServer(models.Model):
    """Configure the oursms sms gateway."""

    _inherit = "sms.mail.server"
    _name = "sms.mail.server"
    _description = "Oursms Gateway"

    username = fields.Char("Username", help="The Username refers to the username for the account in oursms.net")
    password = fields.Char("Password", help="The Password refers to the username for the account in oursms.net")
    token = fields.Char("token", help="The token refers to the username for the account in oursms.net")
    sender = fields.Char("Sender", help="Sender refers to the sender name which should be activated from oursms.net.")


    def test_conn_oursms(self):
        sms_body = "Oursms Test Connection Successful........"
        mobile_number = self.user_mobile_no
        response = send_sms_using_oursms(
            sms_body, mobile_number, sms_gateway=self)
        if response.get('Code') == '100':
                if self.sms_debug:
                    _logger.info(
                        "===========Test Connection status has been sent on %r mobile number", mobile_number)
                raise UserError(
                    "Test Connection status has been sent on %s mobile number" % mobile_number)
        else:
            if self.sms_debug:
                _logger.error(
                    "==========One of the information given by you is wrong. It may be [Mobile Number] or [API KEY]")
            raise UserError(
                "One of the information given by you is wrong. It may be [Mobile Number] or [API Key]")

    @api.model
    def get_reference_type(self):
        selection = super(SmsMailServer, self).get_reference_type()
        selection.append(('oursms', 'OurSms'))
        return selection
