
from odoo import api, fields, models, _
from logging import getLogger
from odoo.exceptions import ValidationError
import logging
from datetime import date,datetime, timedelta
_logger = logging.getLogger(__name__)



class orders(models.Model):
    _name = "orders"
    _table = "orders"
    _inherit = ['mail.thread','mail.activity.mixin']

    user_id = fields.Many2one('res.users', string="Create By:", index=True, tracking=2,
                              default=lambda self: self.env.user, readonly=1)

    vehicleOperatingCodeNumber = fields.Char('Operating Code Number', store=True)
    carModel = fields.Char('Model', groups='base.group_user')
    CarMilage = fields.Char('Odometer (Km)', groups='base.group_user')
    techName = fields.Many2many('hr.employee', string="Employee")
    workStartDate = fields.Datetime(string="Work Start Date", groups='base.group_user')
    customerComm = fields.Text('Driver Complaints', groups='base.group_user')
    ExfinishDate = fields.Datetime(string="Expected Finish Date", groups='base.group_user')
    finishDate = fields.Datetime(string="Completed Date", groups='base.group_user')

    carModel = fields.Char('Vehicle Model', groups='base.group_user')
    # CarMilage = fields.Char('Vehicle Odometer (Km)', groups='base.group_user')
    canelReasonfield = fields.Char('Reason for Cancellation', groups='base.group_user')
    cancelReason = fields.Text('Canclation Reason', groups='base.group_user')
    employeeComplete = fields.Many2one('hr.employee', string="Completed By")
    # raise ValidationError(_("{} after the for\n").format(self.electronicNumer))
    ############################### Vehicle from fleet Module#######################################################################

    model_id_order = fields.Char("Vehicle Name")
    busNameAR_order = fields.Char("Bus Name Arabic")
    busNameEN_order = fields.Char("Bus Name English")
    searialNumbers_order = fields.Char("Serial Number")
    plateNumberAR_order = fields.Char("Plate Number (Arabic)")
    ownerName_order = fields.Char("Owner Name")
    electronicNumer_order = fields.Char("Operating Code Number")
    insuranceName_order = fields.Char("Insurance Name")
    insuranceStartDate_order = fields.Date("Insurance Start Date")
    insuranceEndDate_order = fields.Date("Insurance End Date")
    insurancePrice_order = fields.Char("Insurance Price")
    modelYear_order = fields.Char("Model Year")
    passengerCapacity_order = fields.Char("Passenger Capacity")
    registrationEndDate_order = fields.Date("Registration Expiration Date")
    ownerElectronicumber_order = fields.Char("Electronic Owner Number")
    status_field_order = fields.Char("Vehicle Status")
    # order_count_order = fields.Integer("Number of Orders")

    ##############################Vehicle from accedints Module#######################################################################

    accidentsDescription_acc = fields.Text("Accidents Description")
    accidentsDate_acc = fields.Date("Date of Accidents")
    accidentsAttachment_acc = fields.Many2many('ir.attachment', string="Attachments")
    driver_name_acc = fields.Char("Driver Name")
    ##############################################################################################################
    engineOil_feet = fields.Char("Engine Oil Type")
    engineOilfilter_feet = fields.Char("Oil Filter Type")
    oilCapacity_feet = fields.Char("Engine Oil Capacity Without Filter")
    oilCapacitywith_feet = fields.Char("Engine Oil Capacity With Filter")
    oil_serv_km_fleet = fields.Float("Engine Oil change Every (Km)")
    oil_filter_serv_km_feet = fields.Float("Oil Filter change Every (Km)")
    engineFilter_feet = fields.Float("Air Filter (Km)")


    transOil_feet = fields.Char("Transmission Oil Type")
    transcapacity_feet = fields.Char("Transmission Oil Capacity")
    tr_oil_typ_feet = fields.Float("Transmission Oil change Every (Km)")

    diffOil_fleet = fields.Char("Differential Oil Type")
    diffoilCapacity_fleet = fields.Char("Differential Oil Capacity")
    diffoil_serv_km_fleet = fields.Float("Differential Oil change Every (Km)")


    engineBelts_feet = fields.Float("Engine Belts (Km)")
    tirelife_feet = fields.Float("Tires (Km)")
    batterylife_feet = fields.Float("Battery (Km)")
    brakes_feet = fields.Float("Brakes (Km)")
    acFilters_feet = fields.Float("AC Filter (Km)")
    otherMaint = fields.Char("Other Maintenance")




    @api.onchange('vehicleOperatingCodeNumber')
    def _get_vehicle_info(self):
        fleet_id = self.env['fleet.vehicle'].search([('electronicNumer', '=', self.vehicleOperatingCodeNumber)])
        accedints_ids = self.env['accidents'].search([('electronicNumer_accd', '=', self.vehicleOperatingCodeNumber)])
        maint_ids = self.env['fleet.vehicle'].search([('electronicNumer', '=', self.vehicleOperatingCodeNumber)])


        for fleet_ids in fleet_id:
            self.carModel = fleet_ids.modelYear
            self.busNameAR_order = fleet_ids.busNameAR
            self.busNameEN_order = fleet_ids.busNameEN
            self.searialNumbers_order = fleet_ids.searialNumbers
            self.ownerName_order = fleet_ids.ownerName
            self.electronicNumer_order = fleet_ids.electronicNumer
            self.insuranceName_order = fleet_ids.insuranceName
            self.insuranceStartDate_order = fleet_ids.insuranceStartDate
            self.insuranceEndDate_order = fleet_ids.insuranceEndDate
            self.insurancePrice_order = fleet_ids.insurancePrice
            self.passengerCapacity_order = fleet_ids.passengerCapacity
            self.registrationEndDate_order = fleet_ids.registrationEndDate
            self.ownerElectronicumber_order = fleet_ids.ownerElectronicumber
            self.status_field_order = fleet_ids.status_field
            self.model_id_order = fleet_ids.model_id.name




        for accedints_id in accedints_ids:
            self.accidentsDescription_acc = accedints_id.accidentsDescription
            self.accidentsDate_acc = accedints_id.accidentsDate
            self.accidentsAttachment_acc = accedints_id.accidentsAttachment
            self.driver_name_acc = accedints_id.driver_name

        for maints_id in maint_ids:
            self.engineOil_feet = maints_id.engineOil
            self.engineOilfilter_feet = maints_id.oil_filter
            self.oilCapacitywith_feet = maints_id.oilCapacityWf
            self.oil_serv_km_fleet = maints_id.oil_serv_km

            self.diffOil_fleet = maints_id.diffOil
            self.diffoilCapacity_fleet = maints_id.diffoilCapacity
            self.diffoil_serv_km_fleet = maints_id.diffoil_serv_km


            self.transOil_feet = maints_id.transOil
            self.transcapacity_feet = maints_id.transcapacity
            self.engineFilter_feet = maints_id.engineFilter
            self.engineBelts_feet = maints_id.engineBelts
            self.tirelife_feet = maints_id.tirelife
            self.batterylife_feet = maints_id.batterylife
            self.brakes_feet = maints_id.brakes
            self.acFilters_feet = maints_id.acFilters
            self.oilCapacity_feet = maints_id.oilCapacityOf
            self.oil_filter_serv_km_feet = maints_id.oil_filter_serv_km
            self.tr_oil_typ_feet = maints_id.trans_serv_km


    # order_count = fields.Integer(compute='_order_count', string='# Orders')
    #
    # @api.depends('vehicleOperatingCodeNumber')
    # def _order_count(self):
    #     order_id = self.env['fleet.vehicle'].search([('vehicleOperatingCodeNumber', '=', self.electronicNumer)])
    #     self.order_count = len(order_id)

    ################################################ Vehicle from fleet###########################################################

    ############################### Vehicle from accedints Module#######################################################################


    order_ID = fields.Char(string='Order ID', required=True, readonly=True, default=lambda self: _('New'))
    G="A"

    note = fields.Char(string='')
    @api.model
    def create(self, vals):
        if not vals.get('note'):
             vals['note'] = 'New'
        if vals.get('order_ID', ('New')) == ('New'):
             vals['order_ID'] = self.env['ir.sequence'].next_by_code(
                 'orders') or ('New')
        res = super(orders, self).create(vals)
        return res



    
    def name_get(self):
        result = []
        for record in self:
             record_name = '[' + self.G + '] ' + record.order_ID
             # raise ValidationError(_("{} after the for\n").format(record_name))
             result.append((record.id, record_name))
        return result

    # Diagnosis information entary 


    timeIn = fields.Datetime(string="Time in", groups='base.group_user')
    timeOut = fields.Datetime(string="Time Out", groups='base.group_user')
    odometerIN  = fields.Float('Odometer In (Km)', groups='base.group_user')
    odometerOut =  fields.Float('Odometer Out (Km)', groups='base.group_user')

    fuelLevel = fields.Selection([
     ('ee', 'E'),
     ('1_4','1/4'),
     ('1_2','1/2'),
     ('3_4','3/4'),
     ('ff','F'),
    ], string= 'Fuel Level', tracking= True)

    
    fuelType = fields.Selection([
     ('9_1', '91'),
     ('9_5','95'),
     ('deisel','Diesel'),
    ], string= 'Fuel Type', tracking= True )

   
    
# for orders progressssssssss 
    state = fields.Selection([
    ('draft', 'Draft'),
    ('order_parts','Order Parts'),
    ('in_progress','In Progress'),
    ('on_hold','On Hold'),
    ('complete','Complete'),
    ('cancel','Cancel'),
    
    ], string= 'Order Status', readonly=True, default="draft", help='Choose the state', tracking= True)


    onHold = fields.Char('Reason for Hold', groups='base.group_user')

                                    # inspection info section 
    
    def action_draft(self):
        self.state = 'draft'

    def action_order_parts(self):
        self.state = 'order_parts'

    def action_in_progress(self):
        self.state = 'in_progress'
        
    def action_on_hold(self):
        self.state = 'on_hold'

    def action_complete(self):
        self.state = 'complete'
        actions = self.env.ref('kb_car_workshop_s.completes_wizard').read()[0]
        # raise ValidationError(_("{} after the for\n").format(action))
        return actions

        # groups = "QC GROUP"
        # group = self.env['res.groups'].search([('id', '=', self.env.ref('orders.identifier').id)])

    def action_cancel(self):
        self.state = 'cancel'
        action = self.env.ref('kb_car_workshop_s.create_appointment_wizard').read()[0]
        # raise ValidationError(_("{} after the for\n").format(action))
        return action


        

    #Tire INSPECTON 

    spareTire = fields.Selection([
                                ('Yes','Yes'),
                                ('No','No')], string="Spare Tire", groups='base.group_user')
    tireCondition = fields.Selection([
                                ('tireGood','Good'),
                                ('tirerepair','Repair'),
                                ('tirechange','Change')], string="Tire Condition", groups='base.group_user')



    # vehicle inspection  checklist 
    branch_1 = fields.Char('Branch', groups='base.group_user')
    inpBy_1 = fields.Char('Inspected By', groups='base.group_user')
    driverName = fields.Char('Driver name', groups='base.group_user')


    fw_item = fields.Char('Front Windshield', groups='base.group_user')
    fw_itemGood = fields.Boolean('Good', groups='base.group_user')
    fw_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    fw_change = fields.Boolean('Replace', groups='base.group_user')
    fw_remark = fields.Char('Remarks', groups='base.group_user')


    SGR_item = fields.Char('Side Glass R/L ', groups='base.group_user')
    SGR_itemGood = fields.Boolean('Good', groups='base.group_user')
    SGR_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    SGR_change = fields.Boolean('Replace', groups='base.group_user')
    SGR_remark = fields.Char('Remarks', groups='base.group_user')

    RLM_item = fields.Char('Side Mirror R/L', groups='base.group_user')
    RLM_itemGood = fields.Boolean('Good', groups='base.group_user')
    RLM_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    RLM_change = fields.Boolean('Replace', groups='base.group_user')
    RLM_remark = fields.Char('Remarks', groups='base.group_user')

    RG_item = fields.Char('Rear Glass', groups='base.group_user')
    RG_itemGood = fields.Boolean('Good', groups='base.group_user')
    RG_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    RG_change = fields.Boolean('Replace', groups='base.group_user')
    RG_remark = fields.Char('Remarks', groups='base.group_user')

    PC_item = fields.Char('Passenger Chairs', groups='base.group_user')
    PC_itemGood = fields.Boolean('Good', groups='base.group_user')
    PC_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    PC_change = fields.Boolean('Replace', groups='base.group_user')
    PC_remark = fields.Char('Remarks', groups='base.group_user')

    PCSB_item = fields.Char('Passenger Chairs Seat Belt', groups='base.group_user')
    PCSB_itemGood = fields.Boolean('Good', groups='base.group_user')
    PCSB_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    PCSB_change = fields.Boolean('Replace', groups='base.group_user')
    PCSB_remark = fields.Char('Remarks', groups='base.group_user')

    PDW_item = fields.Char('Passengers Doors Working', groups='base.group_user')
    PDW_itemGood = fields.Boolean('Good', groups='base.group_user')
    PDW_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    PDW_change = fields.Boolean('Replace', groups='base.group_user')
    PDW_remark = fields.Char('Remarks', groups='base.group_user')

    DSG_itemGood = fields.Boolean('Good', groups='base.group_user')
    DSG_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    DSG_change = fields.Boolean('Replace', groups='base.group_user')
    DSG_remark = fields.Char('Remarks', groups='base.group_user')

    BBH_itemGood = fields.Boolean('Good', groups='base.group_user')
    BBH_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    BBH_change = fields.Boolean('Replace', groups='base.group_user')
    BBH_remark = fields.Char('Remarks', groups='base.group_user')

    FB_itemGood = fields.Boolean('Good', groups='base.group_user')
    FB_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    FB_change = fields.Boolean('Replace', groups='base.group_user')
    FB_remark = fields.Char('Remarks', groups='base.group_user')

    RB_itemGood = fields.Boolean('Good', groups='base.group_user')
    RB_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    RB_change = fields.Boolean('Replace', groups='base.group_user')
    RB_remark = fields.Char('Remarks', groups='base.group_user')

    RSB_itemGood = fields.Boolean('Good', groups='base.group_user')
    RSB_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    RSB_change = fields.Boolean('Replace', groups='base.group_user')
    RSB_remark = fields.Char('Remarks', groups='base.group_user')

    LSB_itemGood = fields.Boolean('Good', groups='base.group_user')
    LSB_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    LSB_change = fields.Boolean('Replace', groups='base.group_user')
    LSB_remark = fields.Char('Remarks', groups='base.group_user')

    BSB_itemGood = fields.Boolean('Good', groups='base.group_user')
    BSB_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    BSB_change = fields.Boolean('Replace', groups='base.group_user')
    BSB_remark = fields.Char('Remarks', groups='base.group_user')

    FHL_itemGood = fields.Boolean('Good', groups='base.group_user')
    FHL_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    FHL_change = fields.Boolean('Replace', groups='base.group_user')
    FHL_remark = fields.Char('Remarks', groups='base.group_user')

    IDRL_itemGood = fields.Boolean('Good', groups='base.group_user')
    IDRL_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    IDRL_change = fields.Boolean('Replace', groups='base.group_user')
    IDRL_remark = fields.Char('Remarks', groups='base.group_user')

    BL_itemGood = fields.Boolean('Good', groups='base.group_user')
    BL_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    BL_change = fields.Boolean('Replace', groups='base.group_user')
    BL_remark = fields.Char('Remarks', groups='base.group_user')

    BSL_itemGood = fields.Boolean('Good', groups='base.group_user')
    BSL_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    BSL_change = fields.Boolean('Replace', groups='base.group_user')
    BSL_remark = fields.Char('Remarks', groups='base.group_user')

    Horn_itemGood = fields.Boolean('Good', groups='base.group_user')
    Horn_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    Horn_change = fields.Boolean('Replace', groups='base.group_user')
    Horn_remark = fields.Char('Remarks', groups='base.group_user')

    RA_itemGood = fields.Boolean('Good', groups='base.group_user')
    RA_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    RA_change = fields.Boolean('Replace', groups='base.group_user')
    RA_remark = fields.Char('Remarks', groups='base.group_user')

    RL_itemGood = fields.Boolean('Good', groups='base.group_user')
    RL_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    RL_change = fields.Boolean('Replace', groups='base.group_user')
    RL_remark = fields.Char('Remarks', groups='base.group_user')

    SM_itemGood = fields.Boolean('Good', groups='base.group_user')
    SM_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    SM_change = fields.Boolean('Replace', groups='base.group_user')
    SM_remark = fields.Char('Remarks', groups='base.group_user')

    AC_itemGood = fields.Boolean('Good', groups='base.group_user')
    AC_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    AC_change = fields.Boolean('Replace', groups='base.group_user')
    AC_remark = fields.Char('Remarks', groups='base.group_user')

    ACF_itemGood = fields.Boolean('Good', groups='base.group_user')
    ACF_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    ACF_change = fields.Boolean('Replace', groups='base.group_user')
    ACF_remark = fields.Char('Remarks', groups='base.group_user')

    IVL_itemGood = fields.Boolean('Good', groups='base.group_user')
    IVL_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    IVL_change = fields.Boolean('Replace', groups='base.group_user')
    IVL_remark = fields.Char('Remarks', groups='base.group_user')

    WBWW_itemGood = fields.Boolean('Good', groups='base.group_user')
    WBWW_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    WBWW_change = fields.Boolean('Replace', groups='base.group_user')
    WBWW_remark = fields.Char('Remarks', groups='base.group_user')

    ACB_itemGood = fields.Boolean('Good', groups='base.group_user')
    ACB_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    ACB_change = fields.Boolean('Replace', groups='base.group_user')
    ACB_remark = fields.Char('Remarks', groups='base.group_user')

    EABC_itemGood = fields.Boolean('Good', groups='base.group_user')
    EABC_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    EABC_change = fields.Boolean('Replace', groups='base.group_user')
    EABC_remark = fields.Char('Remarks', groups='base.group_user')

    Refr_itemGood = fields.Boolean('Good', groups='base.group_user')
    Refr_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    Refr_change = fields.Boolean('Replace', groups='base.group_user')
    Refr_remark = fields.Char('Remarks', groups='base.group_user')


    BFB_itemGood = fields.Boolean('Good', groups='base.group_user')
    BFB_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    BFB_change = fields.Boolean('Replace', groups='base.group_user')
    BFB_remark = fields.Char('Remarks', groups='base.group_user')

    HandB_itemGood = fields.Boolean('Good', groups='base.group_user')
    HandB_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    HandB_change = fields.Boolean('Replace', groups='base.group_user')
    HandB_remark = fields.Char('Remarks', groups='base.group_user')

    Oil_itemGood = fields.Boolean('Good', groups='base.group_user')
    Oil_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    Oil_change = fields.Boolean('Replace', groups='base.group_user')
    Oil_remark = fields.Char('Remarks', groups='base.group_user')

    OilF_itemGood = fields.Boolean('Good', groups='base.group_user')
    OilF_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    OilF_change = fields.Boolean('Replace', groups='base.group_user')
    OilF_remark = fields.Char('Remarks', groups='base.group_user')

    WL_itemGood = fields.Boolean('Good', groups='base.group_user')
    WL_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    WL_change = fields.Boolean('Replace', groups='base.group_user')
    WL_remark = fields.Char('Remarks', groups='base.group_user')

    PS_itemGood = fields.Boolean('Good', groups='base.group_user')
    PS_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    PS_change = fields.Boolean('Replace', groups='base.group_user')
    PS_remark = fields.Char('Remarks', groups='base.group_user')

    Gear_itemGood = fields.Boolean('Good', groups='base.group_user')
    Gear_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    Gear_change = fields.Boolean('Replace', groups='base.group_user')
    Gear_remark = fields.Char('Remarks', groups='base.group_user')

    GearOil_itemGood = fields.Boolean('Good', groups='base.group_user')
    GearOil_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    GearOil_change = fields.Boolean('Replace', groups='base.group_user')
    GearOil_remark = fields.Char('Remarks', groups='base.group_user')

    FF_itemGood = fields.Boolean('Good', groups='base.group_user')
    FF_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    FF_change = fields.Boolean('Replace', groups='base.group_user')
    FF_remark = fields.Char('Remarks', groups='base.group_user')

    AF_itemGood = fields.Boolean('Good', groups='base.group_user')
    AF_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    AF_change = fields.Boolean('Replace', groups='base.group_user')
    AF_remark = fields.Char('Remarks', groups='base.group_user')

    TC_itemGood = fields.Boolean('Good', groups='base.group_user')
    TC_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    TC_change = fields.Boolean('Replace', groups='base.group_user')
    TC_remark = fields.Char('Remarks', groups='base.group_user')

    fireExt_itemGood = fields.Boolean('Good', groups='base.group_user')
    fireExt_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    fireExt_change = fields.Boolean('Replace', groups='base.group_user')
    fireExt_remark = fields.Char('Remarks', groups='base.group_user')

    firstAid_itemGood = fields.Boolean('Good', groups='base.group_user')
    firstAid_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    firstAid_change = fields.Boolean('Replace', groups='base.group_user')
    firstAid_remark = fields.Char('Remarks', groups='base.group_user')

    overallClean_itemGood = fields.Boolean('Good', groups='base.group_user')
    overallClean_itemrepair = fields.Boolean('Repair', groups='base.group_user')
    overallClean_change = fields.Boolean('Replace', groups='base.group_user')
    overallClean_remark = fields.Char('Remarks', groups='base.group_user')

    # Order Summary 

    # DATE
    date_1 = fields.Date(string="Date")

    # add photo to order
    attachment_ids = fields.Many2many('ir.attachment', 'car_rent_checklist_ir_attachments_rel', 'rental_id', 'attachment_id', string="Attachments", help="Images of the vehicle")
    #products
    order_line_ids = fields.One2many('order_line','order_id', string="Orders ID")
    #Order Summary
    order_summary_id = fields.One2many('order_summary','order_summary_ids', string="Orders Summary")

    maintenance_items_id = fields.One2many('maintenance_table', 'maintenanceTable_id')

    tire_table_ids = fields.One2many('tires_table', 'tires_table_id')

    battery_table_ids = fields.One2many('battery_table', 'battery_table_id')


###################################################################################

#
# def return_action_to_open_odometers(self):
#         self.ensure_one()
#         domain = [
#             ('vehicleOperatingCodeNumber', '=', self.id)]
#         return {
#             'name': _('orders'),
#             'domain': domain,
#             'res_model': 'orders',
#             'type': 'ir.actions.act_window',
#             'view_id': False,
#             'view_mode': 'tree,form',
#             'view_type': 'form',
#             'help': _('''<p class="oe_view_nocontent_create">
#                            Click to Create for New service
#                         </p>'''),
#             'limit': 80,
#             'context': "{'default_vehicleOperatingCodeNumber': '%s'}" % self.id,
#         }
    order_count = fields.Integer(compute='_order_count', string='# Orders')
    def _order_count(self):
        for each in self:
                order_id = self.env['orders'].search([('vehicleOperatingCodeNumber', '=', self.vehicleOperatingCodeNumber)])
                each.order_count = len(order_id)

    def orders_smart_button(self):
        self.ensure_one()
        domain = [('vehicleOperatingCodeNumber', '=', self.vehicleOperatingCodeNumber)]

        return {
            'name': _('orders'),
            'domain': domain,
            'res_model': 'orders',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'context': "{'default_vehicleOperatingCodeNumber': '%s'}" % self.id,
            }

