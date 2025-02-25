# -*- coding: utf-8 -*-
from xml.dom import ValidationErr
from odoo import api, fields, models, _

class SalemBanks(models.Model):
    _inherit = "res.company"

    bankName1 = fields.Char(string='Bank Name')
    bankimage1 = fields.Image(string='image' )
    IBN1 = fields.Char(string='Bank Iban')
    bankditel=fields.One2many('bank_line','bankditel', string='Bank Accounts')

    



class Saleminvoce(models.Model):
    _inherit ="account.move"

    bankditel = fields.One2many('bank_line','bankditel', string="Bank Accounts")


   

class bank_detial(models.Model):
    _name="bank_line"
    _description = "Bank line"

    bankName1= fields.Char(string='Bank Name')
    bankimage1 = fields.Image(string='image')
    IBN1 = fields.Char(string='Bank Iban')
    bankditel=fields.Many2one('res.company',string='Bank Accounts')
        


    


