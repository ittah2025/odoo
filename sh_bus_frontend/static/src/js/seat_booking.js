odoo.define("sh_bus_frontend.website_event", function (require) {
    var ajax = require("web.ajax");
    $(document).ready(function () {
        $(document).on("click", ".book_ticket", function (ev) {
            var $btn = $(this);
            var search_id = parseInt($btn.attr("data-id"));

            var firstSeatLabel = 1;
            if (search_id) {
                $.post(
                    "/get_booked_seat",
                    {
                        trip_id: search_id,
                    },
                    function (bigData) {
                        bigData = JSON.parse(bigData);
                        var map_list = bigData["data"];
                        var front_seating_map_class = ".front-seating-map-" + search_id;
                        var counter_id = "#counter-" + search_id;
                        var selected_seats_id = "#selected-seats-" + search_id;
                        var total_id = "#total-" + search_id;
                        var currency_symbol_id = "#currency_symbol_" + search_id;
                        var legend = ".legend-" + search_id;
                        var checkout_button_class = ".checkout-button-" + search_id;
                        var go_button_class = ".go-button-" + search_id;
                        var dropping_point_class = ".dropping-point_" + search_id;
                        var boarding_point_class = ".boarding-point_" + search_id;
                        var amenities_list_class = ".amenities_list_" + search_id;
                        if (map_list.length > 0) {
                            var $cart = $(selected_seats_id),
                                $counter = $(counter_id),
                                $total = $(total_id),
                                $currency_symbol = $(currency_symbol_id),
                                sc = $(front_seating_map_class).seatCharts({
                                    map: map_list,
                                    seats: bigData["seats"],
                                    naming: {
                                        top: false,
                                        getLabel: function (character, row, column) {
                                            return firstSeatLabel++;
                                        },
                                    },
                                    legend: {
                                        node: $(legend),
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
                                                .data("seatLabel", this.settings.label)
                                                .data("seatPrice", this.data().price)
                                                .data("seatCateg", this.data().category)
                                                .appendTo($cart);

                                            $counter.text(sc.find("selected").length + 1);
                                            $total.text(recalculateTotal(sc) + this.data().price);
                                            $(checkout_button_class).removeAttr("disabled");

                                            return "selected";
                                        } else if (this.status() == "selected") {
                                            //update the counter
                                            $counter.text(sc.find("selected").length - 1);
                                            //and total
                                            $total.text(recalculateTotal(sc) - this.data().price);

                                            //remove the item from our cart
                                            $("#cart-item-" + this.settings.id).remove();

                                            if (sc.find("selected").length <= 1) {
                                                $(checkout_button_class).attr("disabled", "disabled");
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
                            $(selected_seats_id).on("click", ".cancel-cart-item", function () {
                                sc.get($(this).parents("li:first").data("seatId")).click();
                            });
                            if (bigData["boarding_points"].length > 0) {
                                var boarding_html_data =
                                    '<div class="row" style="align-items: center;"><div class="col-lg-4 col-md-12 col-sm-12 col-12 pl-8 pr-0"><h5 class="bp_text">Boarding Point :</h5></div><div class="col-lg-8 col-md-12 col-sm-12 col-12 pl-0"> <select required="required" id="boarding_point">';
                                $.each(bigData["boarding_points"], function (key, value) {
                                    boarding_html_data += '<option value="' + value[0] + '">' + value[1] + "</option>";
                                });
                                boarding_html_data += '</select><span class="fa fa-caret-down"></span></div></div>';
                                $(boarding_point_class).html(boarding_html_data);
                            }
                            if (bigData["dropping_points"].length > 0) {
                                var dropping_html_data =
                                    '<div class="row" style="align-items: center;"><div class="col-lg-4 col-md-12 col-sm-12 col-12 pl-8 pr-0"><h5 class="dp_text">Dropping Point :</h5></div><div class="col-lg-8 col-md-12 col-sm-12 col-12 pl-0"> <select required="required" id="dropping_point">';
                                $.each(bigData["dropping_points"], function (key, value) {
                                    dropping_html_data += '<option value="' + value[0] + '">' + value[1] + "</option>";
                                });
                                dropping_html_data += '</select><span class="fa fa-caret-down"></span></div></div>';
                                $(dropping_point_class).html(dropping_html_data);
                            }
                            if (bigData["amenities_list"].length > 0) {
                                var amenities_html_data =
                                    '<div class="row"><div class="col-lg-4 col-md-12 col-sm-12 col-12 pl-8 pr-0"><h5 class="am_text">Amenities :</h5></div><div class="col-lg-8 col-md-12 col-sm-12 col-12 pl-0" id="bus_amenities">';
                                $.each(bigData["amenities_list"], function (key, value) {
                                    amenities_html_data += '<span class="amenities_tag">' + value[0] + "</span>";
                                });
                                amenities_html_data += "</div></div>";
                                $(amenities_list_class).html(amenities_html_data);
                            }
                        }

                        $(document).on("click", checkout_button_class, function (ev) {
                            var passenger_info_class = ".passenger_info_" + search_id;
                            var passenger_detail_class = ".passenger-detail_" + search_id;

                            $(passenger_info_class).css("visibility", "visible");
                            $(go_button_class).css("visibility", "visible");

                            var seat_list = [];
                            var html_data = "";
                            var i = 1;
                            $(selected_seats_id)
                                .find("li")
                                .each(function (index) {
                                    seat_list.push($(this).data("seatId"));
                                    html_data += "<tr>";
                                    html_data += '<td ><span class="p_counter">' + i + ".</span></td>";
                                    html_data += '<td><input required="required" type="text" class="mtb-10" name="p_name_' + i + '"></input></td>';
                                    html_data += '<td><input required="required" type="text" class="mtb-10" name="p_email_' + i + '"></input></td>';
                                    html_data += '<td><input required="required" type="number" class="mtb-10" style="width:50%"  min="0" max="100" name="p_age_' + i + '"></input></td>';
                                    html_data += '<td><select class="mtb-10" name="p_gender_' + i + '"><option value="Male">Male</option><option value="Female">Female</option><option value="Child">Children</option></select></td>';
                                    html_data += "</tr>";
                                    i += 1;
                                });
                            $(passenger_detail_class).html(html_data);
                            //										var unavailble_seat_tickettype = {};
                            //										$('.selected-seats').find('li').each(function( index ) {
                            //										  if ($(this).data('seatCateg') in unavailble_seat_tickettype){
                            //												var seat_list = unavailble_seat_tickettype[$(this).data('seatCateg')]
                            //												seat_list.push($(this).data('seatId'))
                            //												unavailble_seat_tickettype[$(this).data('seatCateg')] = seat_list
                            //											}else{
                            //												unavailble_seat_tickettype[$(this).data('seatCateg')] = [$(this).data('seatId')]
                            //											}
                            //
                            //										});
                            //										ev.preventDefault();
                            //								        ev.stopPropagation();
                            //								        var $form = $(ev.currentTarget).closest('form');
                            //								        var $button = $(ev.currentTarget).closest('[type="submit"]');
                            //								            $button.attr('disabled', true);
                            //
                            //								            return ajax.jsonRpc($form.attr('action'), 'call', {'unavailble_seat_tickettype':unavailble_seat_tickettype}).then(function (modal) {
                            //								                var $modal = $(modal);
                            //								                $modal.modal({backdrop: 'static', keyboard: false});
                            //								                $modal.find('.modal-body > div').removeClass('container'); // retrocompatibility - REMOVE ME in master / saas-19
                            //								                $modal.appendTo('body').modal();
                            //								                $modal.on('click', '.js_goto_event', function () {
                            //								                    $modal.modal('hide');
                            //								                    $button.prop('disabled', false);
                            //								                });
                            //								                $modal.on('click', '.close', function () {
                            //								                    $button.prop('disabled', false);
                            //								                });
                            //								            });
                        });
                        $(document).on("click", go_button_class, function (ev) {
                            var data_list = [];
                            var i = 1;
                            var count = false;
                            $(selected_seats_id)
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
                                    "/add_cart_ticket",
                                    {
                                        data_list: JSON.stringify(data_list),
                                        search_trip_id: JSON.stringify(search_id),
                                    },
                                    function (bigData) {
                                        bigData = JSON.parse(bigData);
                                        var sId = bigData["id"];
                                        var base_url = bigData["base_url"];

                                        var redirect_url = base_url + "/mail/view?model=sale.order&res_id=" + sId;
                                        location.href = "/shop/cart";
                                    }
                                );
                            }
                        });
                    }
                );
            }
        });
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
});
