# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.osv import expression
from ast import literal_eval
from datetime import date


class DashboardCompanies(models.Model):
    _name = "dashboard.companies"
    _description = "Dashboard Companies"

    busType = fields.Char(string='Bus Type')
    location = fields.Char(string='Location')
    busModel = fields.Integer(string='Model')
    busNo = fields.Integer(string='No')

    dashboardId = fields.Many2one('companies.info')


class CompaniesInfo(models.Model):
    _name = "companies.info"
    _description = "Companies Information"
    _rec_name = "name"

    logo = fields.Binary()
    companyId = fields.Many2one('res.partner', string='Company Name')
    name = fields.Char(string="Name", help='Name of the Company')
    contractPeriod = fields.Date(string='Contract Period')
    description = fields.Text()

    companiesInfoId = fields.One2many('dashboard.companies', 'dashboardId', string='')
