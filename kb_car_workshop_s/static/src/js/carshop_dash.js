odoo.define('kb_car_workshop_s.dashboard', function (require) {
  "use strict";

  
  var AbstractAction = require('web.AbstractAction');
  var core = require('web.core');
  var QWeb = core.qweb;
  var rpc = require('web.rpc');
  var ajax = require('web.ajax');

  var PosDashboard = AbstractAction.extend({
    xmlDependencies: ['/kb_car_workshop_s/static/src/xml/Dashboard.xml'],
    template: 'Dashboard_Orders',

    
    

    init: function(parent, context) {

      this._super(parent, context);
      this.dashboards_templates = ['Dashboard_Orders'];
      this.today_sale = [];
    },



    start: function() {
      var self = this;
      this.set("title", 'Dashboard');
      return this._super().then(function() { 
          self.render_dashboards();
      });
  },


    render_dashboards: function() {
      var self = this;
      _.each(this.dashboards_templates, function(template) {
          console.log("hello Fares" )
          // self.$('.car_dashboard').append(QWeb.render('EmployeeWarning', {widget: self}));
        });     
 },
  willStart: function() {
    console.log("will start")
       var self = this;
       return $.when(ajax.loadLibs(this), this._super()).then(function() {
            return self.fetch_data();
       });

  },



  
  fetch_data : function() {
    var self = this;
    var def1 = this._rpc({
            model: 'orders',
            method: 'get_data'
    }).then(function(result){
       self.total_cars = result ['total_cars'],
       self.total_order_compleate = result ['total_order_complete'],
       self.total_order_Parts = result ['total_order_parts'],
       self.total_order_onHold= result ['total_order_onHold'],
       self.total_order_inprogress= result ['total_order_inProgres'],
       self.total_orders = result ['total_orders'],
       console.log(self.total_cars)
   });
    return $.when(def1);
  },


  


 });

  core.action_registry.add('custom_dashboard_tag', PosDashboard);

  return PosDashboard;

});