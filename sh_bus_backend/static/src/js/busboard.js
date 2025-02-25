odoo.define("bus_seat_booking_board", function (require) {
    "use strict";

    var core = require("web.core");
    var Widget = require("web.Widget");
    var rpc = require("web.rpc");
    var ajax = require("web.ajax");
    var QWeb = core.qweb;
    var _t = core._t;

    var AbstractAction = require("web.AbstractAction");

    var seatBookingBoard = AbstractAction.extend({
        template: "seatBookingBoard",

        events: {},

        init: function (parent, action) {
            var firstSeatLabel = 1;

            if (action.context && action.context.active_id && action.context.active_model) {
                $.post(
                    "/get_booked_seat_data",
                    {
                        trip_id: action.context.active_id,
                    },
                    function (bigData) {
                        bigData = JSON.parse(bigData);
                        var map_list = bigData["data"];
                        if (map_list.length > 0) {
                            var $cart = $("#selected-seats"),
                                $counter = $("#counter"),
                                $total = $("#total"),
                                $currency_symbol = $("#currency_symbol"),
                                sc = $("#seating-map").seatCharts({
                                    map: map_list,
                                    seats: bigData["seats"],
                                    naming: {
                                        top: false,
                                        getLabel: function (character, row, column) {
                                            return firstSeatLabel++;
                                        },
                                    },
                                    legend: {
                                        node: $("#legend"),
                                        items: bigData["legend_items"],
                                    },
                                    click: function () {
                                        if (this.status() == "available") {
                                            var selected_seat = "R" + this.settings.id.split("_")[0] + " S" + this.settings.id.split("_")[1];
                                            $(
                                                "<li>" +
                                                    this.data().category +
                                                    " Seat # " +
                                                    "<b>" +
                                                    this.settings.label +
                                                    ": $" +
                                                    this.data().price +
                                                    '</b> <a href="#" class="cancel-cart-item"><i class="fa fa-fw o_button_icon fa-close"></i></a></li>'
                                            )
                                                .attr("id", "cart-item-" + this.settings.id)
                                                .data("seatId", this.settings.id)
                                                .data("seatLabel", this.settings.label)
                                                .data("seatPrice", this.data().price)
                                                .data("seatCateg", this.data().category)
                                                .appendTo($cart);

                                            $counter.text(sc.find("selected").length + 1);
                                            $total.text(recalculateTotal(sc) + this.data().price);
                                            $currency_symbol.text(bigData["currency"]);
                                            $(".change-seat-button").removeAttr("disabled");
                                            return "selected";
                                        } else if (this.status() == "selected") {
                                            //update the counter
                                            $counter.text(sc.find("selected").length - 1);
                                            //and total
                                            $total.text(recalculateTotal(sc) - this.data().price);

                                            //remove the item from our cart
                                            $("#cart-item-" + this.settings.id).remove();

                                            if (sc.find("selected").length <= 1) {
                                                $(".change-seat-button").attr("disabled", "disabled");
                                            }

                                            //seat has been vacated
                                            return "available";
                                        } else if (this.status() == "unavailable") {
                                            //seat has been already booked
                                            return "unavailable";
                                        } else {
                                            return this.style();
                                        }
                                    },
                                });
                            sc.get(bigData["booked_seat"]).status("unavailable");
                            $("#selected-seats").on("click", ".cancel-cart-item", function (ev) {
                                ev.preventDefault();
                                sc.get($(this).parents("li:first").data("seatId")).click();
                            });
                            if (bigData["boarding_points"].length > 0) {
                                var boarding_html_data =
                                    '<div class="row"><div class="col-lg-4 col-md-12 col-sm-12 col-12 pl-8 pr-0"><h5 class="bp_text"><b>Boarding Point :</b></h5></div><div class="col-lg-8 col-md-12 col-sm-12 col-12 pl-0"> <select required="required" id="boarding_point">';
                                $.each(bigData["boarding_points"], function (key, value) {
                                    boarding_html_data += '<option value="' + value[0] + '">' + value[1] + "</option>";
                                });
                                boarding_html_data += '</select><span class="fa fa-caret-down"></span></div></div>';
                                $(".boarding-point").html(boarding_html_data);
                            }
                            if (bigData["dropping_points"].length > 0) {
                                var dropping_html_data =
                                    '<div class="row"><div class="col-lg-4 col-md-12 col-sm-12 col-12 pl-8 pr-0"><h5 class="dp_text"><b>Dropping Point :</b></h5></div><div class="col-lg-8 col-md-12 col-sm-12 col-12 pl-0"> <select required="required" id="dropping_point">';
                                $.each(bigData["dropping_points"], function (key, value) {
                                    dropping_html_data += '<option value="' + value[0] + '">' + value[1] + "</option>";
                                });
                                dropping_html_data += '</select><span class="fa fa-caret-down"></span></div></div>';
                                $(".dropping-point").html(dropping_html_data);
                            }
                            if (bigData["amenities_list"].length > 0) {
                                var amenities_html_data =
                                    '<div class="row"><div class="col-lg-4 col-md-12 col-sm-12 col-12 pl-8 pr-0"><h5 class="am_text"><b>Amenities :</b></h5></div><div class="col-lg-8 col-md-12 col-sm-12 col-12 pl-0" id="bus_amenities">';
                                $.each(bigData["amenities_list"], function (key, value) {
                                    amenities_html_data += '<span class="amenities_tag">' + value[0] + "</span>";
                                });
                                amenities_html_data += "</div></div>";
                                $(".amenities_list").html(amenities_html_data);
                            }
                        }

                        $(document).on("click", ".checkout-button", function (ev) {
                            $(".passenger_info").css("visibility", "visible");
                            $(".go-button").css("visibility", "visible");
                            var seat_list = [];
                            var html_data = "";
                            var i = 1;

                            $("#selected-seats")
                                .find("li")
                                .each(function (index) {
                                    seat_list.push($(this).data("seatId"));
                                    html_data += "<tr>";
                                    html_data += '<td ><span class="p_counter">' + i + ".</span></td>";
                                    html_data += '<td><input required="required" type="text" class="mtb-10" name="p_name_' + i + '"></input></td>';
                                    html_data += '<td><input required="required" type="text" class="mtb-10" name="p_email_' + i + '"></input></td>';
                                    html_data += '<td><input required="required" type="number" class="mtb-10"  min="0" max="100" name="p_age_' + i + '"></input></td>';
                                    html_data += '<td><select class="mtb-10" name="p_gender_' + i + '"><option value="Male">Male</option><option value="Female">Female</option><option value="Child">Children</option></select></td>';
                                    html_data += "</tr>";
                                    i += 1;
                                });
                            $(".passenger-detail").html(html_data);
                        });
                    }
                );

                $(document).on("click", ".go-button", function (ev) {
                    var data_list = [];
                    var i = 1;
                    var count = false;

                    $("#selected-seats")
                        .find("li")
                        .each(function (index) {
                            if (count == false) {
                                var seat_list = [];

                                seat_list.push($(this).data("seatId"));
                                seat_list.push($(this).data("seatLabel"));
                                seat_list.push($(this).data("seatPrice"));

                                var name_input = "input[name='p_name_" + i + "']";
                                var email_input = "input[name='p_email_" + i + "']";
                                var age_input = "input[name='p_age_" + i + "']";
                                var gender_input = "select[name='p_gender_" + i + "']";
                                var boarding_point = $("#boarding_point").val() || "";
                                var dropping_point = $("#dropping_point").val() || "";

                                if ($(name_input).val() == "" || $(email_input).val() == "" || $(age_input).val() == "" || $(gender_input).val() == "") {
                                    alert("Please Enter Details !");
                                    count = true;
                                } else {
                                    seat_list.push($(name_input).val());
                                    seat_list.push($(email_input).val());
                                    seat_list.push($(age_input).val());
                                    seat_list.push($(gender_input).val());

                                    seat_list.push(boarding_point);
                                    seat_list.push(dropping_point);

                                    data_list.push(seat_list);

                                    i += 1;
                                }
                            }
                        });

                    if (count == false) {
                        var self = this;
                        $.post(
                            "/next_checkout",
                            {
                                data_list: JSON.stringify(data_list),
                                search_trip_id: JSON.stringify(action.context.active_id),
                            },
                            function (bigData) {
                                bigData = JSON.parse(bigData);
                                var sId = bigData["id"];
                                var base_url = bigData["base_url"];
                                var redirect_url = base_url + "/mail/view?model=sale.order&res_id=" + sId;
                                location.href = redirect_url;
                            }
                        );
                    }
                });
                function recalculateTotal(sc) {
                    var total = 0;
                    //basically find every selected seat and sum its price
                    sc.find("selected").each(function () {
                        total += this.data().price;
                    });
                    return total;
                }

                var _gaq = _gaq || [];
                _gaq.push(["_setAccount", "UA-36251023-1"]);
                _gaq.push(["_setDomainName", "jqueryscript.net"]);
                _gaq.push(["_trackPageview"]);

                (function () {
                    var ga = document.createElement("script");
                    ga.type = "text/javascript";
                    ga.async = true;
                    ga.src = ("https:" == document.location.protocol ? "https://ssl" : "http://www") + ".google-analytics.com/ga.js";
                    var s = document.getElementsByTagName("script")[0];
                    s.parentNode.insertBefore(ga, s);
                })();
                return this._super.apply(this, arguments);
            }
        },

        start: function () {
            var self = this;

            return this.load();
        },

        load: function (dashboards) {
            var self = this;
        },
    });

    core.action_registry.add("busBoard.book", seatBookingBoard);

    return {
        seatBookingBoard: seatBookingBoard,
    };
});

odoo.define("bus_seat_booking_layout_board", function (require) {
    "use strict";

    var core = require("web.core");
    var Widget = require("web.Widget");
    var rpc = require("web.rpc");
    var ajax = require("web.ajax");
    var QWeb = core.qweb;
    var _t = core._t;

    var AbstractAction = require("web.AbstractAction");

    var seatBookingBoard = AbstractAction.extend({
        template: "seatBookingBoardMain",

        events: {},

        init: function (parent, action) {
            var firstSeatLabel = 1;

            if (action.context && action.context.active_id && action.context.active_model) {
                $.post(
                    "/get_json_data_from_registration",
                    {
                        bus_type_id: action.context.active_id,
                    },
                    function (bigData) {
                        bigData = JSON.parse(bigData);
                        var map_list = bigData["data"];
                        if (map_list.length > 0) {
                            var $cart = $("#selected-seats"),
                                $counter = $("#counter"),
                                $total = $("#total"),
                                sc = $("#seat-map").seatCharts({
                                    map: map_list,
                                    seats: bigData["seats"],
                                    naming: {
                                        top: false,
                                        getLabel: function (character, row, column) {
                                            return firstSeatLabel++;
                                        },
                                    },
                                    legend: {
                                        node: $("#legend"),
                                        items: bigData["legend_items"],
                                    },
                                    click: function () {
                                        if (this.status() == "available") {
                                            var selected_seat = "R" + this.settings.id.split("_")[0] + " S" + this.settings.id.split("_")[1];
                                            $(
                                                "<li>" +
                                                    this.data().category +
                                                    " Seat # " +
                                                    "<b>" +
                                                    selected_seat +
                                                    ": $" +
                                                    this.data().price +
                                                    '</b> <a href="#" class="cancel-cart-item"><i class="fa fa-fw o_button_icon fa-close"></i></a></li>'
                                            )
                                                .attr("id", "cart-item-" + this.settings.id)
                                                .data("seatId", this.settings.id)
                                                .data("seatCateg", this.data().category)
                                                .appendTo($cart);

                                            $counter.text(sc.find("selected").length + 1);
                                            $total.text(recalculateTotal(sc) + this.data().price);
                                            $(".change-seat-button").removeAttr("disabled");

                                            return "selected";
                                        } else if (this.status() == "selected") {
                                            //update the counter
                                            $counter.text(sc.find("selected").length - 1);
                                            //and total
                                            $total.text(recalculateTotal(sc) - this.data().price);

                                            //remove the item from our cart
                                            $("#cart-item-" + this.settings.id).remove();

                                            if (sc.find("selected").length <= 1) {
                                                $(".change-seat-button").attr("disabled", "disabled");
                                            }

                                            //seat has been vacated
                                            return "available";
                                        } else if (this.status() == "unavailable") {
                                            //seat has been already booked
                                            return "unavailable";
                                        } else {
                                            return this.style();
                                        }
                                    },
                                });
                            //	 							sc.get(bigData['booked_seat']).status('unavailable');
                            //	 							$('#selected-seats').on('click', '.cancel-cart-item', function () {
                            //	 								sc.get($(this).parents('li:first').data('seatId')).click();
                            //	 							});
                        }

                        $(document).on("click", ".change-seat-button", function (ev) {
                            var seat_list = [];
                            $("#selected-seats")
                                .find("li")
                                .each(function (index) {
                                    seat_list.push($(this).data("seatId"));
                                });
                            if (seat_list.length > 1) {
                                alert("You cannot select more then 1 seat !");
                            } else {
                                $.post(
                                    "/change_seat",
                                    {
                                        event_registration_id: action.context.active_id,
                                        seat_no: seat_list[0],
                                    },
                                    function (bigData) {
                                        location.reload();
                                    }
                                );
                            }
                        });
                    }
                );

                function recalculateTotal(sc) {
                    var total = 0;
                    //basically find every selected seat and sum its price
                    sc.find("selected").each(function () {
                        total += this.data().price;
                    });
                    return total;
                }

                var _gaq = _gaq || [];
                _gaq.push(["_setAccount", "UA-36251023-1"]);
                _gaq.push(["_setDomainName", "jqueryscript.net"]);
                _gaq.push(["_trackPageview"]);

                (function () {
                    var ga = document.createElement("script");
                    ga.type = "text/javascript";
                    ga.async = true;
                    ga.src = ("https:" == document.location.protocol ? "https://ssl" : "http://www") + ".google-analytics.com/ga.js";
                    var s = document.getElementsByTagName("script")[0];
                    s.parentNode.insertBefore(ga, s);
                })();
                return this._super.apply(this, arguments);
            }
        },

        start: function () {
            var self = this;

            return this.load();
        },

        load: function (dashboards) {
            var self = this;
        },
    });

    core.action_registry.add("busBoard.main", seatBookingBoard);

    return {
        seatBookingBoard: seatBookingBoard,
    };
});
