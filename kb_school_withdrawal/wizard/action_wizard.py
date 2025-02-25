from odoo import api, fields, models


class ActionWindow(models.Model):
    _name = "action_button"

    name = fields.Char(string="Name", help="TEST")
    def press_button(self):

        print("123132123")
