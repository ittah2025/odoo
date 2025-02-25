# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2016 Webkul Software Pvt. Ltd.
# Author : www.webkul.com
#
##############################################################################
import logging
import requests
import json
from urllib3.exceptions import HTTPError
from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning

_logger = logging.getLogger(__name__)

def send_sms_using_oursms(body_sms, mob_no, from_mob=None, sms_gateway=None):
    '''
    This function is designed for sending sms using OurSms SMS API.

    :param body_sms: body of sms contains text
    :param mob_no: Here mob_no must be string having one or more number
     seprated by (,)
    :param from_mob: sender mobile number or id used in OurSms API
    :param sms_gateway: sms.mail.server config object for OurSms Credentials
    :return: response dictionary if sms successfully sent else empty dictionary
    '''
    if not sms_gateway or not body_sms or not mob_no:
        return {}
    if sms_gateway.gateway == "oursms":
        if sms_gateway.username and sms_gateway.password and sms_gateway.sender:
            if isinstance(mob_no, list):
                mob_no = ','.join(mob_no)
            mob_no = mob_no.replace('+', '')
            # url = "https://oursms.net/api/sendsms.php"
            url = "https://api.oursms.com/api-a/msgs"
            username = sms_gateway.username
            token = sms_gateway.token
            sender = sms_gateway.sender
            numbers = mob_no
            message = body_sms
            #comp_url = "%s?username=%s&password=%s&sender=%s&numbers=%s&message=%s&unicode=e&Rmduplicated=1&return=json" % (url, username, password, sender, numbers, message)
            comp_url = "%s?username=%s&token=%s&src=%s&dests=%s&body=%s&priority=0&delay=0&validity=0&maxParts=0&dlr=0&prevDups=0&msgClass=promotional" % (url, username, token, sender, numbers, message)
            try:
                response = requests.get(comp_url)
                return response.json()
            except Exception as e:
                _logger.info(
                    "---------------OurSms Exception While Sending SMS -----%r----\
                    -----", e)
    return {}


class SmsSms(models.Model):
    """SMS sending using OurSms SMS Gateway."""

    _inherit = "wk.sms.sms"
    _name = "wk.sms.sms"
    _description = "OurSms SMS"


    def send_sms_via_gateway(
            self, body_sms, mob_no, from_mob=None, sms_gateway=None):
        self.ensure_one()
        gateway_id = sms_gateway if sms_gateway else super(
            SmsSms, self).send_sms_via_gateway(
            body_sms, mob_no, from_mob=from_mob, sms_gateway=sms_gateway)
        if gateway_id:
            if gateway_id.gateway == 'oursms':
                for element in mob_no:
                    for mobi_no in element.split(','):
                        response = send_sms_using_oursms(
                            body_sms, mobi_no, from_mob=from_mob,
                            sms_gateway=gateway_id)
                        message_data = response.get('MessageIs')
                        sms_report_obj = self.env["sms.report"].create(
                            {
                                'to': mobi_no, 'msg': self.msg,
                                'sms_sms_id': self.id,
                                "auto_delete": self.auto_delete,
                                'sms_gateway_config_id': gateway_id.id})
                        vals = {'state':'undelivered'}
                        if response.get('Code') == '100':
                            code = response.get('Code')
                            vals['oursms_sms_id'] = sms_report_obj.id
                            vals['state'] = 'sent'
                            vals['message'] = response.get("MessageIs")
                        else:
                            vals.update({'state': 'failed','message':response.get("MessageIs")})
                        if sms_report_obj:
                            sms_report_obj.write(vals)
                    else:
                        self.write({'state': 'error'})
                else:
                    self.write({'state': 'sent'})
            else:
                gateway_id = super(SmsSms, self).send_sms_via_gateway(
                    body_sms, mob_no, from_mob=from_mob,
                    sms_gateway=sms_gateway)
        else:
            _logger.info(
                "----------------------------- SMS Gateway not found ----------\
                ---------------")
        return gateway_id


class SmsReport(models.Model):
    """SMS report."""

    _inherit = "sms.report"

    oursms_sms_id = fields.Char("OurSms SMS ID")

    @api.model
    def cron_function_for_sms(self):
        _logger.info(
            "************** Cron Function For OurSms SMS *******************")
        all_sms_report = self.search([('state', 'in', ('sent', 'new')),('sms_gateway','=','oursms')])
        for sms in all_sms_report:
            sms_sms_obj = sms.sms_sms_id if sms.sms_sms_id else False
            if not sms.oursms_sms_id:
                sms.send_now()
        super(SmsReport, self).cron_function_for_sms()
        return True

    def send_sms_via_gateway(
            self, body_sms, mob_no, from_mob=None, sms_gateway=None):
        self.ensure_one()
        gateway_id = sms_gateway if sms_gateway else super(
            SmsReport, self).send_sms_via_gateway(
            body_sms, mob_no, from_mob=from_mob, sms_gateway=sms_gateway)
        if gateway_id:
            if gateway_id.gateway == 'oursms':
                if mob_no:
                    for element in mob_no:
                        count = 1
                        for mobi_no in element.split(','):
                            if count == 1:
                                self.to = mobi_no
                                rec = self
                            else:
                                rec = self.create({
                                    'to': mobi_no, 'msg': body_sms,
                                    "auto_delete": self.auto_delete,
                                    'sms_gateway_config_id': gateway_id.id})
                            response = send_sms_using_oursms(
                                body_sms, mobi_no, from_mob=from_mob,
                                sms_gateway=gateway_id)
                            message_data = response.get('MessageIs')
                            vals = {'state':'undelivered'}
                            if response.get('MessageIs') in ['Success']:
                                code = response.get("Code")
                                vals['oursms_sms_id'] = rec.id
                                vals['state'] = 'sent'
                                vals['message'] = response.get('MessageIs')
                            else:
                                vals.update({'state': 'failed','message':response.get("MessageIs")})
                            rec.write(vals)
                            count += 1
                else:
                    self.write({'state': 'sent'})
            else:
                gateway_id = super(SmsReport, self).send_sms_via_gateway(
                    body_sms, mob_no, from_mob=from_mob,
                    sms_gateway=sms_gateway)
        return gateway_id

    def get_sms_count(sms_gateway=None):
       username = sms_gateway.username
       password = sms_gateway.password
       url = "https://api.oursms.com/api-a/billing/credits" 

       comp_url = "%s?username=%s&password=%s" % (url, username, password)
       try:
            response = requests.get(comp_url)
            return response.json()
       except Exception as e:
            _logger.info(
                "---------------OurSms Exception While Sending SMS -----%r----\
                -----", e)
              
