# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2019 OM Apps 
#    Email : omapps180@gmail.com
#################################################

from odoo import api, models, fields, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    def copy_account_line(self):
        for line in self:
            line_id = line.with_context(default_account_id=line.account_id.id).copy()
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
