odoo.define('kb_Tahtheeb_school.student_grade_marks', function (require) {
    'use strict';
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    var _t = core._t;
    var StudentGradeMarks = AbstractAction.extend({
    template: 'StudentGradeMarks',
        events: {
            'click .grade-back-page': '_onBack',
        },
        
        init: function(parent, action) {
            this._super(parent, action);
            this.rec = action.context.rec || action.context.active_id;
        },
        start: function() {
            var self = this;
            self.load_data();
            return this._super();
        },
        load_data: function () {
            var self = this;
                    console.log('this.getSession()',this.getSession())
            self._rpc({
                        model: 'studentassessment',
                        method: 'get_student_grade',
                        args: [[self.rec]],
                    }).then(function(datas) {
                    console.log("dataaaaaa", datas)
                        self.$('.table_view').html(QWeb.render('StudentGradeMarksResult', {
                                   report_lines : datas,
                        }));
                    });
            },
        _onBack: function (ev) {
            var self = this;
            this._rpc({
                        route: '/web/action/load',
                        params: {
                            action_id: 'kb_Tahtheeb_school.student_assessment_action',
                        },
            }).then(function(r) {
                        r.res_id = self.rec;
                        r.view_mode = 'form';
                        r.views=  [[false, 'form']];
                        return self.do_action(r,{clear_breadcrumbs: true,})
            });
        },
    });
    core.action_registry.add("student_grade_marks", StudentGradeMarks);
    return StudentGradeMarks;
});