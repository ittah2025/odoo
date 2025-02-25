# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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
{
    "name":  "OurSms SMS Gateway",
    "summary":  """Send sms notifications using Oursms SMS Gateway.""",
    "category":  "Marketing",
    "version":  "1.0.0",
    "sequence":  1,
    "author":  "Webkul Software Pvt. Ltd.",
    "license":  "Other proprietary",
    "website":  "https://store.webkul.com/",
    "description":  """https://store.webkul.com/""",
    "live_test_url":  "https://store.webkul.com/",
    "depends":  [
        'sms_notification',
    ],
    "data":  [
        'views/oursms_config_view.xml',
        'views/sms_report.xml',
        'edi/sms_template_for_sending_payment_link.xml',
    ],
    "images":  ['static/description/Banner.gif'],
    "application":  True,
    "installable":  True,
    "auto_install":  False,
    "price":  0,
    "currency":  "USD",
    "pre_init_hook":  "pre_init_check",
    "external_dependencies": {
        'python': ['urllib3'],
    },
}
