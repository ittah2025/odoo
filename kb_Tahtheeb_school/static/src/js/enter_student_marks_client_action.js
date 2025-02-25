odoo.define('kb_Tahtheeb_school.std_assessment_marks', function (require) {
    'use strict';
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    var _t = core._t;
    var StudentAssessment = AbstractAction.extend({
        template: 'StudentAssessment',
        events: {
            'click .save_student_record': '_onSave',
            'click .save-all': '_onSaveAll',
            'click .back-page': '_onBack',
            'change .hw-number': '_onChangeTotalhw',
            'change .cw-number': '_onChangeTotalcw',
            'change .cp-number': '_onChangeCP',
            'change .semester': '_onChangesemester',
            'input .input_cw': '_onInputcw',
            'input .mid-semester': '_onInputmid',
            'input .final-semester': '_onInputfinal',
            'keypress .input_cw': '_onKeypress',
        },

        
        init: function (parent, action) {
            this._super(parent, action);
            this.rec = action.context.rec || action.context.active_id;
        },
        willStart: function(){
            var self = this;
            var def = this._rpc({
                model: 'studentassessment',
                method: 'search_read',
                kwargs: {
                    domain: [['id','=',this.rec]],
                    fields: ['state'],
                },
            })
            .then(function (datas) {
                if (datas[0].state == 'locked') {
                    self._onBack();
                    self.displayNotification({
                        type: 'danger',
                        message: _t('Assessment Cannot be Changed \n Once Locked!'),
                        sticky: false
                    });
                }
            });
            return Promise.all([this._super.apply(this, arguments), def]);
        }, 
        start: function () {
            var self = this;
            self.load_data();
            return this._super();
        },
        load_data: function () {
            var self = this;
            self._rpc({
                model: 'studentassessment',
                method: 'get_students',
                args: [[self.rec]],
            }).then(function (datas) {
                    self.$('.table_view').html(QWeb.render('SaleTable', {
                        report_lines: datas,
                    }));
            });
        },
        _onSave: function (event) {
            var $tr = $(event.target).parent().parent()

            var marks_vals = {}
            var line_vals = {}
            var line_id = 0
            $tr.find('td').each(function (Index, e) {
                if ($(e).find("span").hasClass("student-id")) {
                    line_id = $(e).find("span").data('id')
                } else if ($(e).find("span").hasClass("cp-number")) {
                    var cp_val = $(e).find("span").find('select').children('option:selected').val()
                    if (cp_val == "N/A") {
                        marks_vals['cp'] = -1
                    }else {
                        marks_vals['cp'] = cp_val
                    }
                } else if ($(e).find("span").hasClass("cw-number")) {
                    var line_val = line_vals[$(e).find("span").data('id')]
                    if (line_val) {
                        line_val.cw = $(e).find("span").find("input").val()
                    } else {
                        line_vals[$(e).find("span").data('id')] = { 'hw': 0, 'cw': $(e).find("span").find("input").val() }
                    }
                } else if ($(e).find("span").hasClass("hw-number")) {
                    var line_val = line_vals[$(e).find("span").data('id')]
                    var hw_val = $(e).find("span").find('select').children('option:selected').val() 
                    if (line_val) {
                        if (hw_val == "N/A") {
                            line_val.hw = -1
                        } else{
                            line_val.hw = hw_val
                        }
                    } else {
                        if (hw_val == "N/A") {
                            line_vals[$(e).find("span").data('id')] = { 'hw': -1, 'cw': 0 }
                        }else {
                            line_vals[$(e).find("span").data('id')] = { 'hw': hw_val, 'cw': 0 }
                        }
                    }
                } else if ($(e).find("span").hasClass("semester")) {
                    if ($(e).find("span").find("input").hasClass("mid-semester")) {
                        marks_vals['mid_sem'] = $(e).find("span").find("input").val()
                    } else if ($(e).find("span").find("input").hasClass("final-semester")) {
                        marks_vals['final_sem'] = $(e).find("span").find("input").val()
                    }
                }

            });
            var line_list = []
            _.each(line_vals, (line, e) => {
                line_list.push(Array(1, parseInt(e), line));
            });
            marks_vals['student_assessment_line_marks_ids'] = line_list
            this._rpc({
                model: 'student.assessment.line',
                method: 'write',
                args: [[parseInt(line_id)], marks_vals],
            })
            this.displayNotification({
                type: 'info',
                message: _t('Record Has Been Succcessfully Saved!'),
                sticky: false
            });
        },
        _onInputmid : function(ev) {
            var $e = $(ev.target)
            var inputfloat = parseFloat($e.val());
            var input = inputfloat.toString()
            if (input == "NaN"){
                $(ev.target).val('');
            }
            if (inputfloat < 0 || inputfloat > 20){
                $(ev.target).val('');
            }else if (input.includes(".")){
                if (input.indexOf(".")) {
                    var x = input.split(".");
                    var decimal_val = {'2':2,'5':5,'7':7,'25':25,'50':50,'75':75}
                    if (x[1].length != 1 & !(x[1] in decimal_val)) {
                        $(ev.target).val('');
                    }else if (x[1].length == 1  & !(x[1] in decimal_val)) {
                        $(ev.target).val('');
                    }
                }

            }
        },
        _onInputfinal : function(ev) {
            var $e = $(ev.target)
            var inputfloat = parseFloat($e.val());
            
            var input = inputfloat.toString()
            if (input == "NaN"){
                $(ev.target).val('');
            }
            if (inputfloat < 0 || inputfloat > 40){
                $(ev.target).val('');
            }else if (input.includes(".")){
                if (input.indexOf(".")) {
                    var x = input.split(".");
                    var decimal_val = {'2':2,'5':5,'7':7,'25':25,'50':50,'75':75}
                    if (x[1].length != 1 & !(x[1] in decimal_val)) {
                        $(ev.target).val('');
                    }else if (x[1].length == 1  & !(x[1] in decimal_val)) {
                        $(ev.target).val('');
                    }
                }

            }
        },
       
        _onInputcw : function(ev,txt) {
            var $e = $(ev.target)
            // var patt = /^\d{1,10}(\.\d{1,2})?$/;
            var patt2 = /^[+-]?([0-9]+\.?[0-9]*|\.[0-9]+)$/;
            if (!patt2.test($e.val())){
                $(ev.target).val('')
            }else{
                var fp = parseFloat($(ev.target).val())
                var len = $e[0].value.length
                if (fp < 0 || fp > 10){
                    $(ev.target).val($e[0].value.slice(0,len-1))
                }else{
                    $(ev.target).val($e.val())
                }
            }
            var inputfloat = parseFloat($(ev.target).val())
            var input = inputfloat.toString()
            var final_value = ""
            final_value = input
            if (input.includes(".")){
                if (input.indexOf(".")) {
                    var x = input.split(".");
                    var len = $e[0].value.length
                    var decimal_val = {'2':2,'5':5,'7':7,'25':25,'50':50,'75':75}
                    if (x[1].length != 1 & !(x[1] in decimal_val)) {
                        $(ev.target).val($e[0].value.slice(0,len-1));
                        final_value = '';
                    }else if (x[1].length == 1  & !(x[1] in decimal_val)) {
                        $(ev.target).val($e[0].value.slice(0,len-1));
                    }
                }
            }
        },
        _onKeypress: function(event) {
            // var $this = $(this);
            var $this = $(event.target)
            var len = $this[0].value.length
            if ($this[0].value < 0 || $this[0].value > 10){
                $(event.target).val($this[0].value.slice(0,len-1));
            }
            if ((event.which != 46 || $this.val().indexOf('.') != -1) &&
            ((event.which < 48 || event.which > 57) &&
            (event.which != 0 && event.which != 8))) {
                event.preventDefault();
            }
            var text = $(event.target).val();
            if ((event.which == 46) && (text.indexOf('.') == -1)) {
                setTimeout(function() {
                    if ($this.val().substring($this.val().indexOf('.')).length > 3) {
                        $this.val($this.val().substring(0, $this.val().indexOf('.') + 3));
                    }
                }, 1);
            }
            if ((text.indexOf('.') != -1) &&
                (text.substring(text.indexOf('.')).length > 2) &&
                (event.which != 0 && event.which != 8) &&
                ($(event.target)[0].selectionStart >= text.length - 2)) {
                    event.preventDefault();
            }
        },

        _onBack: function (ev) {
            var self = this;
                    this._rpc({
                        route: '/web/action/load',
                        params: {
                            action_id: 'kb_Tahtheeb_school.student_assessment_action',
                        },
                        // here
                    }).then(function(r) {
                        r.res_id = self.rec;
                        r.view_mode = 'form';
                        r.views=  [[false, 'form']];
                        return self.do_action(r,{clear_breadcrumbs: true,})
                    });
        },

        _onChangeTotalhw: function (ev) {
            var $tr = $(ev.target).parent().parent().parent()
            var $current_span = $(ev.target).parent()
            var total_hw = 0.00
            var counter = 0
            var hw_na_counter = 0
            var line_mark_vals = {}
            var id = $current_span.data("id")
            $tr.find('td').each(function (Index, e) {
                if ($(e).find("span").hasClass("hw-number")) {
                    total_hw += parseInt($(e).find("span").find('select').children('option:selected').val());
                    counter += 1
                }
            })
            if ($current_span.find('select').children('option:selected').val() == "N/A") {
                line_mark_vals['hw'] = -1
            }else {
                line_mark_vals['hw'] = $current_span.find('select').children('option:selected').val()

            }
            this.rpcLineMarks(id,line_mark_vals,"HW");
            this.sumUp($tr, total_hw, counter, '.hw-number-total');
            var total_sum = 0.00
            this.totalMarksCalculations($tr, total_sum)
        },

        _onChangeTotalcw: function (ev) {
            var $tr = $(ev.target).parent().parent().parent()
            var $current_span = $(ev.target)
            var total_cw = 0.00
            var counter = 0
            var line_mark_vals = {}
            var id = $current_span.parent().data("id")
            $tr.find('td').each(function (Index, e) {
                if ($(e).find("span").hasClass("cw-number")) {
                    total_cw += parseFloat($(e).find("span").find("input").val());
                    counter += 1
                }
            })
            if (parseFloat($current_span.val()) === -1){
                line_mark_vals['cw'] = -1
            }else{
                line_mark_vals['cw'] = parseFloat($current_span.val())
            }
            this.rpcLineMarks(id,line_mark_vals,"CW");
            this.sumUp($tr, total_cw, counter, '.cw-number-total');
            var total_sum = 0.00
            this.totalMarksCalculations($tr, total_sum)
        },

        _onChangeCP: function (ev) {
            var total_sum = 0.00
            var $tr = $(ev.target).parent().parent().parent()
            var line_id = 0
            var marks_vals = {}
            this.totalMarksCalculations($tr, total_sum)
            $tr.find('td').each(function (Index, e) {
                if ($(e).find("span").hasClass("cp-number")) {
                    line_id = $(e).find("span").data('id')
                    if ($(e).find("span").find('select').children('option:selected').val() == "N/A") {
                        marks_vals['cp'] = -1
                    }else{
                        marks_vals['cp'] = $(e).find("span").find('select').children('option:selected').val() 
                    }
                }
            });
            this._rpc({
                model: 'student.assessment.line',
                method: 'write',
                args: [[parseInt(line_id)], marks_vals],
            })
        },
        _onChangesemester: function (ev) {
            var $current = $(ev.target).parent()
            var line_id = 0
            var marks_vals = {}
            if ($current.hasClass("semester")) {
                line_id = $current.data('id')
                if ($current.find("input").hasClass("mid-semester")) {
                    marks_vals['mid_sem'] = parseFloat($current.find("input").val())
                } else if ($current.find("input").hasClass("final-semester")) {
                    marks_vals['final_sem'] = parseFloat($current.find("input").val())
                }
            }
            this._rpc({
                model: 'student.assessment.line',
                method: 'write',
                args: [[parseInt(line_id)], marks_vals],
            })
        },

        sumUp: function ($tr, total, counter, class1) {
            var avg = Math.ceil(((total / counter)) * 4) / 4;
            
            $tr.find(class1).text(avg);
        },
        rpcLineMarks: function (id,line_mark_vals,work) {
            // var msg = work + ' Record Has Been Succcessfully Saved!'
            var def = this._rpc({
                model: 'student.assessment.line.marks',
                method: 'write',
                args: [[parseInt(id)], line_mark_vals],
            })
            return def;
        },
        totalMarksCalculations: function ($tr, total_sum) {
            $tr.find('td').each(function (index, e) {

                if ($(e).find("span").hasClass("cp-number")) {
                    total_sum += parseFloat($(e).find("span").find('select').children("option:selected").val());
                }
                if ($(e).find("span").hasClass("hw-number-total")) {
                    total_sum += parseFloat($(e).find("span").text());
                }
                if ($(e).find("span").hasClass("cw-number-total")) {
                    total_sum += parseFloat($(e).find("span").text());
                }
            })
            $tr.find('.total-marks').text(total_sum)
        },
        _onSaveAll: function (e) {
           console.log ("onSaveAll===========e.target====",e.target)
        },
    });
    core.action_registry.add("std_assessment_marks", StudentAssessment);
    return StudentAssessment;
});