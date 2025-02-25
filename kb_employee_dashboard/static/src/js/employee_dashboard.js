odoo.define("kb_employee_dashboard.EmployeeDashboard", function (require) {
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;
    var web_client = require('web.web_client');
    var session = require('web.session');
    var ajax = require('web.ajax');
    var _t = core._t;
    var rpc = require('web.rpc');
    var self = this;
    var DashBoard = AbstractAction.extend({
        contentTemplate: 'EmployeeDashboard',

        init: function (parent, context) {
            this._super(parent, context);
            this.dashboard_templates = ['MainSection'];
            this.employeeData = {};  // Initialize employeeData

        },
        start: function () {
            var self = this;
            this.set("title", 'Employee Dashboard');
            return this._super().then(function () {
                self.render_dashboards();
            });
        },
        willStart: function () {
            var self = this;
            return this._super()
        },
        render_dashboards: function () {
            var self = this;
            var templates = []
            var templates = ['MainSection'];
            _.each(templates, function (template) {
                self.$('.o_hr_dashboard').append(QWeb.render(template, {widget: self}))
            });
            // Add onclick events on cards
            self.$('.time-off-card').on('click', function () {
                self.viewTimeOff();
            });
                self.$('.ticket-card').on('click', function () {
                self.viewTicket();
            });
            self.$('.project-card').on('click', function () {
                self.viewProject();
            });
            self.$('.contract-card').on('click', function () {
                self.viewContract();
            });
            self.$('.payslip-card').on('click', function () {
                self.viewPayslip();
            });
            self.$('.more-attendance').on('click', function () {
                self.viewAttendance();
            });
            self.$('.salary_report').on('click', function () {
                self.salaryReport();
            });
            self.$('#btnRight').on('click', function (e) {
                var selectedOpts = $('#xassignees option:selected');
                if (selectedOpts.length == 0) {
                    alert("Nothing to move.");
                    e.preventDefault();
                }

                $('#lstBox2').append($(selectedOpts).clone());
                $(selectedOpts).remove();
                e.preventDefault();
            });
            self.$('#btnLeft').click(function (e) {
                console.log("LEFT")
                var selectedOpts = $('#lstBox2 option:selected');
                if (selectedOpts.length == 0) {
                    alert("Nothing to move.");
                    e.preventDefault();
                }

                $('#xassignees').append($(selectedOpts).clone());
                $(selectedOpts).remove();
                e.preventDefault();
            });

//            meeting move to list
            self.$('#AttendsRight').on('click', function (e) {
                var selectedOpts2 = $('#xpartner option:selected');
                if (selectedOpts2.length == 0) {
                    alert("Nothing to move.");
                    e.preventDefault();
                }

                $('#AttendsBox2').append($(selectedOpts2).clone());
                $(selectedOpts2).remove();
                e.preventDefault();
            });
            self.$('#AttendsLeft').click(function (e) {
                var selectedOpts2 = $('#AttendsBox2 option:selected');
                if (selectedOpts2.length == 0) {
                    alert("Nothing to move.");
                    e.preventDefault();
                }

                $('#xpartner').append($(selectedOpts2).clone());
                $(selectedOpts2).remove();
                e.preventDefault();
            });

//            end meeting move to list
            self.fetch_data()
            self.fetchAttendanceData();
            self.fetchAllocationeData();
            self.fetchPartners();
            self.fetchUsers();
            self.fetchProject();

            self.$('.submit-report').on('click', function () {
                var selectedReport = self.$('.report-selection').val();

                if (selectedReport === 'medical_insurance_request') {
                    self.openReport('kb_hr_forms.print_medical_insurance_request');
                } else if (selectedReport === 'effective_date_notice') {
                    self.openReport('kb_hr_forms.print_effective_date_notice');
                } else if (selectedReport === 'leave_application_request') {
                    self.openReport('kb_hr_forms.laf');
                } else if (selectedReport === 'emplyment_contract') {
                    self.openReportContract('kb_hr_forms.print_emplyment_contract');
                } else if (selectedReport === 'final_settlement') {
                    self.openReportContract('kb_hr_forms.print_final_settlement');
                } else if (selectedReport === 'resignation_form') {
                    self.openReportContract('kb_hr_forms.print_resignation_form');
                } else if (selectedReport === 'print_disclaimer_argeement') {
                    self.openReportContract('kb_hr_forms.print_disclaimer_argeement');
                } else if (selectedReport === 'print_clearance_form') {
                    self.openReportContract('kb_hr_forms.print_clearance_form');
                } else if (selectedReport === 'rdf') {
                    self.openReportContract('kb_hr_forms.rdf');
                } else if (selectedReport === 'nrr') {
                    self.openReportContract('kb_hr_forms.nrr');
                } else if (selectedReport === 'fev') {
                    self.openReportContract('kb_hr_forms.fev');
                } else if (selectedReport === 'eerv') {
                    self.openReportContract('kb_hr_forms.eerv');
                } else if (selectedReport === 'ror') {
                    self.openReportContract('kb_hr_forms.ror');
                } else if (selectedReport === 'cfev') {
                    self.openReportContract('kb_hr_forms.cfev');
                } else if (selectedReport === 'job_offer') {
                    self.openReportContract('kb_hr_forms.job_offer');
                } else {
                }
            });

            self.$('.ask-for-loan').on('click', function () {
                self.createLoan();

            });


            self.$('.ask-for-resignation').on('click', function () {
                self.createResignation();

            });



            self.$('.ask-for-meeting').on('click', function () {
                self.createMeeting();

            });

            self.$('.ask-for-tasking').on('click', function () {
                self.createTasking();

            });

        },


//        Salary Reports
        salaryReport: function () {
            var self = this;
            var nsender = document.getElementById("nsender").value;
            const reportsalary = [];
            reportsalary[0] = nsender;
            this._rpc({
                model: 'hr.employee',
                method: 'create_salary_report',
                args: [reportsalary]
            })
//            .then(function (result) {
//               $('.employee-name').text(result.employee.name);
//
//                });
        },

        // to create loan
        createLoan: function () {
            var self = this;
            var lamount = document.getElementById("lamount").value;
            var installments = document.getElementById("installments").value;
            var sdate = document.getElementById("sdate").value;
            const loans = [];
            loans[0] = lamount;
            loans[1] = installments;
            loans[2] = sdate;
            this._rpc({
                model: 'hr.employee',
                method: 'create_loan',
                args: [loans]
            })
                .then(function (result) {
                    $('.employee-name').text(result.employee.name);

                });
            if (loans[0] && loans[1] && loans[2]) {
                this.displayNotification({message: _t('Your request is submitted'), type: 'success'});
                window.location.reload();
            }
        },

        // to create Resignation
        createResignation: function () {
            var self = this;
            var rdate = document.getElementById("rdate").value;
            var sreason = document.getElementById("sreason").value;
            const resignation = [];
            resignation[0] = rdate;
            resignation[1] = sreason;
            this._rpc({
                model: 'hr.employee',
                method: 'createResignation',
                args: [resignation]
            })
                .then(function (result) {
                    $('.employee-name').text(result.employee.name);

                });
            this.displayNotification({message: _t('Your request is submitted'), type: 'success'});
            window.location.reload();
        },



        fetchPartners: function () {
            var self = this;
            this._rpc({
                model: 'hr.employee',
                method: 'get_all_partners',
            })
                .then(function (result) {
                    var $partnerSelect = self.$('.partner-selection');
                    console.log("partner")
                    result.forEach(function (partner) {
                        $partnerSelect.append('<option value="' + partner.id + '">' + partner.name + '</option>');
                    });
                });
        },

        fetchUsers: function () {
            var self = this;
            this._rpc({
                model: 'hr.employee',
                method: 'get_all_users',
            })
                .then(function (result) {
                    var $userSelect = self.$('.user-selection');
                    result.forEach(function (user) {
                        $userSelect.append('<option value="' + user.id + '">' + user.name + '</option>');
                    });
                });
        },

        fetchProject: function () {
            var self = this;
            this._rpc({
                model: 'hr.employee',
                method: 'get_all_project',
            })
                .then(function (result) {
                    var $projectSelect = self.$('.project-selection');
                    result.forEach(function (project) {
                        $projectSelect.append('<option value="' + project.id + '">' + project.name + '</option>');
                    });
                });
        },


        // to create Meeting
        createMeeting: function () {
            var self = this;
            var msubject = document.getElementById("msubject").value;
            var startingdate = document.getElementById("startingdate").value;
            var startingtime = document.getElementById("startingtime").value;
            var endingdate = document.getElementById("endingdate").value;
            var endingtime = document.getElementById("endingtime").value;
            var attbox2 = document.getElementById("AttendsBox2");
            var listbox = [];
            var i;
            for (i = 0; i < attbox2.length; i++) {
                listbox[i] = attbox2.options[i].value;
            }
            const meeting = [];
            meeting[0] = msubject;
            meeting[1] = startingdate;
            meeting[2] = startingtime;
            meeting[3] = endingdate;
            meeting[4] = endingtime;
            this._rpc({
                model: 'hr.employee',
                method: 'create_meeting',
                args: [listbox, meeting]
            })

            this.displayNotification({message: _t('Your request is submitted'), type: 'success'});
        },

        // to create Task
        createTasking: function () {
            var self = this;
            var ttitle = document.getElementById("ttitle").value;
            var xassignees = document.getElementById("xassignees").value;
            var xprojects = document.getElementById("xprojects").value;
            var x = document.getElementById("lstBox2");
            var txt = [];
            var i;
            for (i = 0; i < x.length; i++) {
                txt[i] = x.options[i].value;
            }
            console.log(txt)
            const tasking = [];
            tasking[0] = ttitle;
            tasking[1] = xassignees;
            tasking[2] = xprojects;
            this._rpc({
                model: 'hr.employee',
                method: 'create_task',
                args: [txt, tasking]
            })

            this.displayNotification({message: _t('Your request is submitted'), type: 'success'});
        },

        // to view time off
        viewTimeOff: function () {
            var self = this;
            this._rpc({
                model: 'hr.employee',
                method: 'get_data',
            })
                .then(function (result) {
                    var employeeData = result.employee;
                    var employeeID = employeeData.id;
                    self.do_action({
                        type: 'ir.actions.act_window',
                        name: 'Time Off',
                        res_model: 'hr.leave',
                        view_mode: 'tree,form',
                        views: [[false, 'list'], [false, 'form']],
                        target: 'current',
                        domain: [['employee_id', '=', employeeID]],
                        context: {
                            'search_default_employee_id': employeeID,
                        },
                    });
                });
        },

        // move to next
//        $(document).ready(function() {
//        self.$('#btn1').click(function(e) {
//        console.log("XXXXXX")
//        }
//            var selectedOpts = $('#lstBox1 option:selected');
//            if (selectedOpts.length == 0) {
//                alert("Nothing to move.");
//                e.preventDefault();
//            }
//
//            $('#lstBox2').append($(selectedOpts).clone());
//            $(selectedOpts).remove();
//            e.preventDefault();
//            });
//
//            $('#btnLeft').click(function(e) {
//                var selectedOpts = $('#lstBox2 option:selected');
//                if (selectedOpts.length == 0) {
//                    alert("Nothing to move.");
//                    e.preventDefault();
//                }
//
//                $('#lstBox1').append($(selectedOpts).clone());
//                $(selectedOpts).remove();
//                e.preventDefault();
//            });
//        });

        viewTicket: function () {
            var self = this;
            this._rpc({
                model: 'hr.employee',
                method: 'get_data',
            })
                .then(function (result) {
                    console.log("Employee Data:", result);
                    var userID = result.employee.user_id;
                    self.do_action({
                        type: 'ir.actions.act_window',
                        name: 'My Helpdesk',
                        res_model: 'help.ticket',
                        view_mode: 'tree,form',
                        views: [[false, 'kanban'], [false, 'form'], [false, 'list']],
                        target: 'current',
                        domain: [['assigned_user', '=', userID]],
                    });
                });
        },


        viewProject: function () {
            var self = this;
            this._rpc({
                model: 'hr.employee',
                method: 'get_data',
            })
                .then(function (result) {
                    console.log("Employee Data:", result);
                    var userID = result.employee.user_id;
                    self.do_action({
                        type: 'ir.actions.act_window',
                        name: 'My Tasks',
                        res_model: 'project.task',
                        view_mode: 'tree,form',
                        views: [[false, 'kanban'], [false, 'form'], [false, 'list']],
                        target: 'current',
                        domain: [['user_ids', '=', userID]],
                    });
                });
        },


        // to view contract
        viewContract: function () {
            var self = this;
            this._rpc({
                model: 'hr.employee',
                method: 'get_data',
            })
                .then(function (result) {
                    var employeeData = result.employee;
                    var employeeID = employeeData.id;
                    self.do_action({
                        type: 'ir.actions.act_window',
                        name: 'Contract',
                        res_model: 'hr.contract',
                        view_mode: 'tree,form',
                        views: [[false, 'list'], [false, 'form']],
                        target: 'current',
                        domain: [['employee_id', '=', employeeID]],
                    });
                });
        },
        // to view payslip
        viewPayslip: function () {
            var self = this;
            this._rpc({
                model: 'hr.employee',
                method: 'get_data',
            })
                .then(function (result) {
                    var employeeData = result.employee;
                    var employeeID = employeeData.id;
                    self.do_action({
                        type: 'ir.actions.act_window',
                        name: 'Payslip',
                        res_model: 'hr.payslip',
                        view_mode: 'tree',
                        views: [[false, 'list'], [false, 'form']],
                        target: 'current',
                        domain: [['employee_id', '=', employeeID]],
                    });
                });
        },
        // to view attendance
        viewAttendance: function () {
            var self = this;
            this._rpc({
                model: 'hr.employee',
                method: 'get_data',
            })
                .then(function (result) {
                    var employeeData = result.employee;
                    var employeeID = employeeData.id;
                    self.do_action({
                        type: 'ir.actions.act_window',
                        name: 'Attendance',
                        res_model: 'hr.attendance',
                        view_mode: 'tree,form',
                        views: [[false, 'list'], [false, 'form']],
                        target: 'current',
                        domain: [['employee_id', '=', employeeID]],
                        context: {
                            'search_default_employee_id': employeeID,
                        },
                    });
                });
        },
        // fetch employee data
        fetch_data: function () {
            var self = this
            var def1 = this._rpc({
                model: 'hr.employee',
                method: "get_data",
            })
                .then(function (result) {
                    var employeeData = result.employee;
                    // console.log(employeeData.attendance.id)
                    $('.employee-name').text(employeeData.name);
                    $('.employee-job').text(employeeData.job);
                    $('.employee-department').text(employeeData.department);
                    $('.employee-manager').text(employeeData.parent_id);
                    $('.payslip-count').text(employeeData.payslip_count);
                    $('.employee-time-off').text(employeeData.allocation_display + '/' + employeeData.allocation_remaining_display);
                    $('.employee-contract').text(employeeData.contract_count);
                    $('.employee-task').text(employeeData.task_count);
                    $('.employee-ticket').text(employeeData.ticket_count);
                    // Append image
                    if (employeeData && employeeData.image) {
                        var $userImage = $('<img>').attr('src', 'data:image/png;base64,' + employeeData.image);
                        $('#employee-img').append($userImage);
                    } else {
                        // default image
                        var $defaultImage = $('<img>').attr('src', 'kb_employee_dashboard/static/src/img/avatar.png');
                        $('#employee-img').append($defaultImage);
                    }
                });
        },
        // fetch attendance data
        fetchAttendanceData: function () {
            var self = this

            function formatHoursMinutes(decimalHours) {
                var hours = Math.floor(decimalHours);
                var minutes = Math.round((decimalHours - hours) * 60);

                var formattedHours = hours < 10 ? '0' + hours : hours;
                var formattedMinutes = minutes < 10 ? '0' + minutes : minutes;

                return formattedHours + ':' + formattedMinutes;
            }

            function formatDateAndTime(dateTimeString) {
                if (!dateTimeString) {
                    return {date: '', time: ''};
                }

                var dateTime = new Date(dateTimeString);
                // Add 2 hours to the date and time
                dateTime.setHours(dateTime.getHours() + 2);
                // Format the date as MM/DD/YYYY
                var formattedDate = (dateTime.getMonth() + 1).toString().padStart(2, '0') + '/' +
                    dateTime.getDate().toString().padStart(2, '0') + '/' +
                    dateTime.getFullYear();
                // Format the time as HH:mm:ss
                var formattedTime = dateTime.getHours().toString().padStart(2, '0') + ':' +
                    dateTime.getMinutes().toString().padStart(2, '0') + ':' +
                    dateTime.getSeconds().toString().padStart(2, '0');

                return {date: formattedDate, time: formattedTime};
            }

            var def1 = this._rpc({
                model: 'hr.attendance',
                method: "get_last_five_records",
            })
                .then(function (result) {
                    if (!result || result.length === 0) {
                        $('.attend-body').append('<p class="text-danger h3 m-5">' + _t('No attendance yet') + '</p>');
                        // $('.attend-body').append('<p class="text-danger h3 m-5">No attendance yet</p>');
                    } else {
                        _.each(result, function (record) {
                            var formattedWorkedHours = formatHoursMinutes(record.worked_hours);
                            var formattedCheckIn = formatDateAndTime(record.check_in);
                            var formattedCheckOut = formatDateAndTime(record.check_out);
                            $('.attend-body').append(
                                '<tr>' +
                                '    <th scope="row">' + formattedCheckIn.date + '</th>' +
                                '    <td>' + formattedCheckIn.time + '</td>' +
                                '    <td>' + formattedCheckOut.time + '</td>' +
                                '    <td>' + formattedWorkedHours + '</td>' +
                                '</tr>'
                            );
                        });
                    }
                });

        },
        // fetch allocation data
        fetchAllocationeData: function () {
            var self = this

            var def1 = this._rpc({
                model: 'hr.leave.allocation',
                method: "get_alloctions",
            })
                .then(function (result) {
                    console.log(result)
                    if (!result || result.length === 0) {
                        $('.my-allocations').append('<p class="text-danger text-center m-5 h3">' + _t('There is no vacation balance yet') + '</p>');
                    } else {
                        _.each(result.allocations, function (record) {
                            $('.my-alloctions').append(
                                '<div class="mt-4 h4"> <span class="text-white">' + record.holiday_status_id + '</span>' +
                                '<span class="text-danger"> : ' + record.max_leaves + '</span>' +
                                '<span class="text-danger"> / ' + (record.max_leaves - record.leaves_taken) + '</span> </div>'
                            );
                        });
                        var totalBalancePercentage = (result.remaining_balance / result.total_balance) * 100;
                        var circle = $('.progress-ring__circle');
                        var circumference = parseFloat(circle.css('stroke-dasharray'));
                        var strokeDasharray = (totalBalancePercentage / 100) * circumference;
                        var strokeDashoffset = circumference - strokeDasharray;

                        circle.css({
                            'stroke-dasharray': strokeDasharray,
                            'stroke-dashoffset': strokeDashoffset
                        });

                        $('.percentage').text(result.total_balance + '/' + result.remaining_balance);
                    }
                });
        },
        // Print Reports
        openReport: function (reportName) {
            var self = this;

            self._rpc({
                model: 'hr.employee',
                method: 'get_data',
            }).then(function (result) {
                if (result && result.employee) {
                    var employeeID = result.employee.id;

                    var additionalData = {
                        docs: [],
                    };

                    self.do_action({
                        type: 'ir.actions.report',
                        report_type: 'qweb-pdf',
                        report_name: reportName,
                        context: {
                            active_ids: [employeeID],
                            docs: additionalData.docs,
                        },
                    });
                } else {
                    console.error("Error: Invalid response from server");
                }
            }).catch(function (error) {
                console.error("Error fetching employee data:", error);
            });
        },

        openReportContract: function (reportName) {
            var self = this;

            self._rpc({
                model: 'hr.contract',
                method: 'get_contract_data',
            }).then(function (result) {
                if (result && result.employee) {
                    var employee = result.employee;

                    var additionalData = {
                        docs: [],
                    };

                    self.do_action({
                        type: 'ir.actions.report',
                        report_type: 'qweb-pdf',
                        report_name: reportName,
                        context: {
                            active_ids: [employee.id],
                            docs: additionalData.docs,
                        },
                    });
                } else {
                    console.error("Error: Invalid response from server");
                }
            }).catch(function (error) {
                console.error("Error fetching employee data:", error);
            });
        },
    });
    core.action_registry.add('dashboard_dashboard_tag', DashBoard);
    return DashBoard;
});