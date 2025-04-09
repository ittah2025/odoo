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


class SchoolWeb(http.Controller):


    @http.route('/registration_request', type="http", auth="public", website=True)
    def registration_request(slef, **kw):
        country_id = request.env['res.country'].sudo().search([])
        company_id = request.env['school.school'].sudo().search([])
        return http.request.render('school.create_registration_request', {'country_id':country_id,'company_id':company_id})

    @http.route('/create/thank_you', type="http", auth="public", website=True,csrf=False)
    def create_registration_request(self, **kw):
        studentfind = request.env['student.student'].sudo().search([('idr_number','=',kw.get('NID'))])
        if studentfind:

            country_id = request.env['res.country'].sudo().search([])
            company_id = request.env['school.school'].sudo().search([])
            return http.request.render('school.create_registration_request',
                                       {'country_id': country_id, 'company_id': company_id})
        else:


            fullstudentname= kw.get('Firstname') +' '+ kw.get('Fathername') +' '+ kw.get('Grandfather') +' '+ kw.get('Familyname')
            fullstudentnameen = kw.get('name_en_1') + ' ' + kw.get('name_en_2') + ' ' + kw.get('name_en_3') + ' ' + kw.get('name_en_4')


            ############################################## Father Information  ##############################################
            fatherFullName = kw.get('firstnamefather') + ' ' + kw.get('fathernamefather') + ' ' + kw.get('grandfathernamefather') + ' ' + kw.get('familynamefather')
            fatherfind = request.env['school.parent'].sudo().search([('father_nat_id', '=', kw.get('NIDfather'))], limit=1)

            if fatherfind:
                fatherID = fatherfind
            else:
                ValFather={
                    'name_arabic_1': kw.get('firstnamefather'),
                    'name_arabic_2': kw.get('fathernamefather'),
                    'name_arabic_3': kw.get('grandfathernamefather'),
                    'name_arabic_4': kw.get('familynamefather'),
                    'name': fatherFullName,
                    'name_en_1': kw.get('name_en_1'),
                    'name_en_2': kw.get('name_en_2'),
                    'name_en_3': kw.get('name_en_3'),
                    'name_en_4': kw.get('name_en_4'),
                    'status': fullstudentnameen,
                    'nationality': 'Saudi',
                    'working_address': '',
                    'father_nat_id': kw.get('NIDfather'),
                    'email': kw.get('emailFather'),
                    'phone' : kw.get('phoneFather'),
                }

                requst_order = request.env['school.parent']
                fatherID = request.env['school.parent'].sudo().create(ValFather)
                fatherID = request.env['school.parent'].sudo().search([('id', '=', fatherID.id)], limit=1)


                ############################################## End Father Information  ##############################################

            
            ############################################## Mother Information  ##############################################
            motherFullName = kw.get('firstnamemother') + ' ' + kw.get('fathernamemother') + ' ' + kw.get('grandfathernamemother') + ' ' + kw.get('familynamemother')
            motherfind = request.env['school.parent'].sudo().search([('father_nat_id', '=', kw.get('NIDmother'))], limit=1)

            if motherfind:
                motherID = motherfind
            else:
                ValMother={
                    'name_arabic_1': kw.get('firstnamemother'),
                    'name_arabic_2': kw.get('fathernamemother'),
                    'name_arabic_3': kw.get('grandfathernamemother'),
                    'name_arabic_4': kw.get('familynamemother'),
                    'name': motherFullName,
                    'name_en_1': kw.get('name_en_1'),
                    'name_en_2': kw.get('name_en_2'),
                    'name_en_3': kw.get('name_en_3'),
                    'name_en_4': kw.get('name_en_4'),
                    'status': fullstudentnameen,
                    'nationality': kw.get('Nationalitymother'),
                    'working_address': '',
                    'father_nat_id': kw.get('NIDmother'),
                    'email': kw.get('emailmother'),
                    'phone' : kw.get('phonemother'),
                }

                requst_order = request.env['school.parent']
                motherID = request.env['school.parent'].sudo().create(ValMother)
                motherID = request.env['school.parent'].sudo().search([('id', 'in', [motherID.id, fatherID.id])])


                ############################################## End Father Information  ##############################################

            # print('father')
            # print(fatherID.id)



            valStdeunt={
                'name_arabic_1':kw.get('Firstname'),
                'name_arabic_2': kw.get('Fathername'),
                'name_arabic_3':kw.get('Grandfather'),
                'name_arabic_4':kw.get('Familyname'),
                'name_en_1': kw.get('name_en_1'),
                'name_en_2': kw.get('name_en_2'),
                'name_en_3': kw.get('name_en_3'),
                'name_en_4': kw.get('name_en_4'),
                'name':fullstudentname,
                'name_arabic': fullstudentnameen,
                'idr_number':kw.get('NID'),
                'email':kw.get('email'),
                'phone':kw.get('phone'),
                'gender': 'male',
                'parent_id' : motherID,
                'father_nat_id' : kw.get('NIDfather'),
                # 'Nationality':kw.get('Nationality'),
                'date_of_birth':kw.get('datebirthday'),
                # 'attachment': kw.get('Previousschool'),
                'city': kw.get('city'),
                'country_id': kw.get('country_id'),
                'street': kw.get('street'),
                'zip': kw.get('Postal'),
                'home_number': kw.get('Additional'),
                # 'school_transportation': kw.get('school_transportation'),
                # 'Educational_system': kw.get('Educational_system'),
                'school_id': kw.get('company_id'),
                #
                # # Father
                # 'firstnamefather': kw.get('firstnamefather'),
                # 'fathernamefather': kw.get('fathernamefather'),
                # 'grandfathernamefather': kw.get('grandfathernamefather'),
                # 'familynamefather': kw.get('familynamefather'),
                # 'fullfathername': fullfathername,
                # 'NIDfather': kw.get('NIDfather'),
                # 'emailFather': kw.get('emailFather'),
                # 'phoneFather': kw.get('phoneFather'),
                # 'NationalityFather': kw.get('NationalityFather'),
                # #mother
                # 'firstnamemother': kw.get('firstnamemother'),
                # 'fathernamemother': kw.get('fathernamemother'),
                # 'grandfathernamemother': kw.get('grandfathernamemother'),
                # 'familynamemother': kw.get('familynamemother'),
                # 'fullmothername': fullmathername,
                # 'NIDmother': kw.get('NIDmother'),
                # 'emailmother': kw.get('emailmother'),
                # 'phonemother': kw.get('phonemother'),
                # 'Nationalitymother': kw.get('Nationalitymother'),
                # #relative
                # 'namerelative' :kw.get('namerelative'),
                # 'relativerelation':kw.get('relativerelation'),
                'emergency_phone' :kw.get('Phonerelative'),
            }

            requst_order = request.env['student.student']
            requstId = request.env['student.student'].sudo().create(valStdeunt)


            # This is method to send an email with the new registration
            # requstId.activity_button_fun()

            # invoice_doc = 'ufile'
            # self.upload_attachment(invoice_doc, requst_order, requstId) # Call upload_attachment method to upload Invoice document
            return request.render("school.registration_thanks", {})

    def upload_attachment(self, file_feild, model, rec_id):
        ''' This method to take a module object and object id to create and store
            attacment and link thim to the new record'''
        files = request.httprequest.files.getlist(file_feild)
        result = {'success': _("All files uploaded")}
        # out = """<script language="javascript" type="text/javascript">
        #     var win = window.top.window;
        #     win.jQuery(win).trigger(%s);
        # </script>"""
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

        # return out % (json.dumps(result))

        return "Files uploaded successfully!"



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


