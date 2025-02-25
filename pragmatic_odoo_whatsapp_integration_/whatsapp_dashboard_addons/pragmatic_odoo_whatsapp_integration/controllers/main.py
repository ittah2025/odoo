from odoo import http
from odoo.http import request
import json


class Conversation(http.Controller):

    @http.route('/web#action=164&cids=1&menu_id=115', type='http', auth='public')
    def conversation_info(self, **kwargs):
        try:
            users = request.env['facebook.messenger'].sudo().search([])
            #sql = request.env.cr.execute("select name from patient_prescription")
            #return "Thanks for watching"
        except:
            return "<h1>Can't access API</h1>"

        return request.render("pragmatic_odoo_whatsapp_integration.conversations.Sidebar", {'patients': users})
    
    @http.route('/whatsapp_dashboard/get_default_answers', type='json', auth="public")
    def get_answer_data(self):
        answers = request.env['chat.answers'].sudo().search([('show', '=', True)])
        question_answers_list = []
        question_answers_json = {}
        for answer in answers:
            if answer.type == "image":
                answer_dict = {answer.name: answer.attachment_ids.ids}
                question_answers_json[answer.name] = answer.attachment_ids.ids
                question_answers_list.append(answer_dict)
            else:
                answer_dict = {answer.name: answer.text}
                question_answers_json[answer.name] = answer.text
                question_answers_list.append(answer_dict)

        return question_answers_json

    @http.route('/whatsapp_dashboard/search_input_chart', type='json', auth="public", website=True)
    def dashboard_search_input_chart(self, search_input, model_name):
        # dashboard_id = request.env[model_name].search([('name', '=', search_input)])
        search_item_ids = request.env[model_name].sudo().search(
            [('name', 'ilike', search_input)])
        search_item_list = []
        if search_item_ids:
            for search_item in search_item_ids:
                # all_values = json.dumps(search_item)
                # print(all_values)
                all_fields = request.env[model_name].sudo().fields_get()
                search_item_dict = {}
                for field in all_fields:
                    search_item_dict[field] = search_item.read([field])[0][field]
                search_item_list.append(search_item_dict)
        return search_item_list

    @http.route('/whatsapp_dashboard/remove_search_chart', type='json', auth="public", website=True)
    def dashboard_search_show_all_chart(self, model):
        search_item_ids = request.env[model].sudo().search([], limit=20)

        search_item_list = []
        if search_item_ids:
            for search_item in search_item_ids:
                # all_values = search_item.sudo().get_values()
                all_fields = request.env[model].fields_get()
                search_item_dict = {}
                for field in all_fields:
                    search_item_dict[field] = search_item.read([field])[0][field]
                search_item_list.append(search_item_dict)
        return search_item_list

    @http.route('/whatsapp/get_message_dashboard', type='json', auth='public')
    def get_dashboard_data(self):
        whatsapp = request.env['ir.module.module'].sudo().search([('name', '=', 'pragtech_whatsapp_messenger')])
        if whatsapp:
            if whatsapp.state == 'installed':
                messages = request.env['whatsapp.messages'].sudo().search([])
                data_list = []
                bar_measure_data_list = []
                bar_label_data_list = ["Sent", "Delivered", "Read"]
                sent_count = 0
                delivered_count = 0
                read_count = 0
                for message in messages:
                    # date_time = message.time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                    # bar_measure_data_list.append(date_time)
                    if message.msg_status == 'sent':
                        sent_count+=1
                    elif message.msg_status == 'delivered':
                        delivered_count+=1
                    elif message.msg_status == 'read':
                        read_count+=1
                data_list.append(sent_count)
                data_list.append(delivered_count)
                data_list.append(read_count)
                data_dict = {
                            'name': "message status",
                            'data': data_list
                        }
                bar_measure_data_list.append(data_dict)
                return_dict = {
                                'data_list': bar_measure_data_list,
                                'model_label_list': bar_label_data_list,
                            }
                pie_dict = {
                    'data_list': data_list,
                    'model_label_list': bar_label_data_list,
                }
                chart_data = json.dumps(return_dict)
                pie_data = json.dumps(pie_dict)
                return_dict = [{
                        'id': 1,
                        'name': "Whatsapp messages status",
                        'chart_theme': "dark",
                        'color_palette': "palette1",
                        'chart_type': "column",
                        'chart_data': chart_data,
                        'chart_background_color': "#fff",
                        'chart_fore_color': "#373d3f",
                        'chart_dashboard_positions': "",
                        'is_distributed_chart': False,
                    },
                    {
                        'id': 2,
                        'name': "Whatsapp messages status",
                        'chart_theme': "dark",
                        'color_palette': "palette1",
                        'chart_type': "pie",
                        'chart_data': pie_data,
                        'chart_background_color': "#fff",
                        'chart_fore_color': "#373d3f",
                        'chart_dashboard_positions': "",
                    }]
                return return_dict
        else:
            sent_count = 0
            delivered_count = 0
            read_count = 0
            data_list = []
            bar_measure_data_list = []
            bar_label_data_list = ["Sent", "Delivered", "Read"]
            data_list.append(sent_count)
            data_list.append(delivered_count)
            data_list.append(read_count)
            data_dict = {
                        'name': "message status",
                        'data': data_list
                    }
            bar_measure_data_list.append(data_dict)
            return_dict = {
                            'data_list': bar_measure_data_list,
                            'model_label_list': bar_label_data_list,
                        }
            chart_data = json.dumps(return_dict)
            return_list = [{
                        'id': 1,
                        'name': "Whatsapp messages status",
                        'chart_theme': "dark",
                        'color_palette': "palette1",
                        'chart_type': "column",
                        'chart_data': chart_data,
                        'chart_background_color': "#fff",
                        'chart_fore_color': "#373d3f",
                        'chart_dashboard_positions': "",
                        'is_distributed_chart': False,
                    },
                    {
                        'id': 2,
                        'name': "Whatsapp messages status",
                        'chart_theme': "dark",
                        'color_palette': "palette1",
                        'chart_type': "pie",
                        'chart_data': chart_data,
                        'chart_background_color': "#fff",
                        'chart_fore_color': "#373d3f",
                        'chart_dashboard_positions': "",
                        'is_distributed_chart': False,
                    }]
            return return_list

