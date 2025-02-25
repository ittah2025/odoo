from odoo import http,_

from odoo.exceptions import ValidationError, UserError
from odoo.http import request
from werkzeug.exceptions import NotFound

import json
import unicodedata
import pprint
import base64
import logging

_logger = logging.getLogger(__name__)


class School(http.Controller):


    @http.route('/registration_request', type="http", auth="public", website=True)
    def registration_request(slef, **kw):
        country_id = request.env['res.country'].sudo().search([])
        company_id = request.env['res.company'].sudo().search([])
        return http.request.render('kb_Tahtheeb_school.creat_registration_request', {'country_id':country_id,'company_id':company_id})
    
    @http.route('/create/thank_you', type="http", auth="public", website=True,csrf=False)
    def create_registration_request(self, **kw):
        studentfind = request.env['registrationrequest'].sudo().search([('NID','=',kw.get('NID'))])
        if studentfind:
            country_id = request.env['res.country'].sudo().search([])
            company_id = request.env['res.company'].sudo().search([])
            return http.request.render('kb_Tahtheeb_school.creat_registration_request',
                                       {'country_id': country_id, 'company_id': company_id})
        else:
            fullstudentname= kw.get('Firstname') +' '+ kw.get('Fathername') +' '+ kw.get('Grandfather') +' '+ kw.get('Familyname')
            fullfathername= kw.get('firstnamefather') + ' '+ kw.get('fathernamefather') +' '+ kw.get('grandfathernamefather') +' '+ kw.get('familynamefather')
            fullmathername= kw.get('firstnamemother') +' '+ kw.get('fathernamemother') +' '+ kw.get('grandfathernamemother') +' '+ kw.get('familynamemother')
            val={
                'Firstname':kw.get('Firstname'),
                'Fathername': kw.get('Fathername'),
                'Grandfathername':kw.get('Grandfather'),
                'Familyname':kw.get('Familyname'),
                'fullstudentname':fullstudentname,
                'NID':kw.get('NID'),
                'email':kw.get('email'),
                'phone':kw.get('phone'),
                'Nationality':kw.get('Nationality'),
                'birthdayDate':kw.get('datebirthday'),
                'attachment': kw.get('Previousschool'),
                'city': kw.get('city'),
                'country_id': kw.get('country_id'),
                'street': kw.get('street'),
                'Postal': kw.get('Postal'),
                'Additional': kw.get('Additional'),
                'school_transportation': kw.get('school_transportation'),
                'Educational_system': kw.get('Educational_system'),
                'company_id': kw.get('company_id'),

                # Father
                'firstnamefather': kw.get('firstnamefather'),
                'fathernamefather': kw.get('fathernamefather'),
                'grandfathernamefather': kw.get('grandfathernamefather'),
                'familynamefather': kw.get('familynamefather'),
                'fullfathername': fullfathername,
                'NIDfather': kw.get('NIDfather'),
                'emailFather': kw.get('emailFather'),
                'phoneFather': kw.get('phoneFather'),
                'NationalityFather': kw.get('NationalityFather'),
                #mother
                'firstnamemother': kw.get('firstnamemother'),
                'fathernamemother': kw.get('fathernamemother'),
                'grandfathernamemother': kw.get('grandfathernamemother'),
                'familynamemother': kw.get('familynamemother'),
                'fullmothername': fullmathername,
                'NIDmother': kw.get('NIDmother'),
                'emailmother': kw.get('emailmother'),
                'phonemother': kw.get('phonemother'),
                'Nationalitymother': kw.get('Nationalitymother'),
                #relative
                'namerelative' :kw.get('namerelative'),
                'relativerelation':kw.get('relativerelation'),
                'Phonerelative' :kw.get('Phonerelative'),
            }
            requst_order=request.env['registrationrequest']
            requstId=request.env['registrationrequest'].sudo().create(val)
            requstId.activity_button_fun()

            invoice_doc = 'ufile'
            self.upload_attachment(invoice_doc, requst_order, requstId) # Call upload_attachment method to upload Invoice document
            return request.render("kb_Tahtheeb_school.registration_thanks", {})

    def upload_attachment(self, file_feild, model, rec_id):
        ''' This method to take a module object and object id to create and store
            attacment and link thim to the new record'''
        files = request.httprequest.files.getlist(file_feild)
        result = {'success': _("All files uploaded")}
        out = """<script language="javascript" type="text/javascript">
            var win = window.top.window;
            win.jQuery(win).trigger(%s);
        </script>"""
        att_vals = []
        for ufile in files:
            try:
                # print("getting data from formfilesfiles: ", pprint.pformat(ufile.read()))
                filename = ufile.filename
                mimetype = ufile.content_type
                if request.httprequest.user_agent.browser == 'safari':
                    # Safari sends NFD UTF-8 (where é is composed by 'e' and [accent])
                    # we need to send it the same stuff, otherwise it'll fail
                    filename = unicodedata.normalize('NFD', ufile.filename)
                rec_id.sudo().write({'attachments':[(0,0,{
                        'name': filename,
                        'res_model': model._name,
                        'res_id': int(rec_id),
                        'mimetype': mimetype,
                        'datas': base64.encodebytes(ufile.read()),
                    })]})
            except Exception:
                result = {'error': str(Exception)}
                _logger.exception("Fail to upload attachment %s" % ufile.filename)
                raise ValidationError(_("Fail to upload attachment %s" % ufile.filename))
        # val = {'attachments': att_vals}
        # rec_id.sudo().write(val)

        return out % (json.dumps(result))



    # @http.route('/registration_course_request', type="http", auth="public", website=True)
    # def registration_course_request(slef, **kw):
    #     course_id = request.env['course'].sudo().search([])
    #     country_id = request.env['res.country'].sudo().search([])
    #     return http.request.render('kb_div_school.creat_registration_course_request', {'course_id':course_id,'country_id':country_id})
    #
    #
    # @http.route('/create/Thank_you', type="http", auth="public", website=True, csrf=False)
    # def create_registration_course_request(slef, **kw):
    #     val = {
    #         'name': kw.get('name'),
    #         'NID': kw.get('NID'),
    #         'email': kw.get('email'),
    #         'phone': kw.get('phone'),
    #         'Nationality': kw.get('Nationality'),
    #         'Gender': kw.get('Gender'),
    #         'course_id': kw.get('course_id'),
    #         'user_type':kw.get('user_type'),
    #         'birthdayDate': kw.get('datebirthday'),
    #         'city': kw.get('city'),
    #         'country_id': kw.get('country_id'),
    #     }
    #
    #     request.env['regestrationcourse'].sudo().create(val)
    #     return request.render("kb_div_school.registration_course_thanks", {})
    #
    # @http.route('/SignUp_Teacher', type="http", auth="public", website=True)
    # def SignUp_Teacher_request(slef, **kw):
    #     return http.request.render('kb_div_school.SignUp_for_Teacher', {})
    #
    # @http.route('/Create/Thank_you', type="http", auth="public", website=True, csrf=False)
    # def create_Registration_request_teacher(slef, **kw):
    #     if  kw.get('yourpassword') == kw.get('ConfirmPassword'):
    #         val = {
    #             'Firstname': kw.get('Firstname'),
    #             'Lastname': kw.get('Lastname'),
    #             'NID': kw.get('NID'),
    #             'email': kw.get('email'),
    #             'phone': kw.get('phone'),
    #             'Gender': kw.get('Gender'),
    #             'Nationality': kw.get('Nationality'),
    #             'yourpassword': kw.get('yourpassword'),
    #         }
    #
    #         request.env['registration_request_teacher'].sudo().create(val)
    #         return request.render("kb_div_school.registration_course_thanks", {})
    #
    #     else:
    #         return http.request.render('kb_div_school.SignUp_for_Teacher', {})


