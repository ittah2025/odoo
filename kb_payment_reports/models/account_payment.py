from odoo import models,fields, api, _
from num2words import num2words


class InvoiceReport(models.AbstractModel):
    _inherit = 'account.payment'

   
    cash_cheque_no = fields.Char("Cash/Cheque No")

    def amount_to_text_custom(self, amount, lang_code):
        num = round(amount, 2)
        if lang_code == 'ar':
            # num = num + 0.0000000000001
            words = num2words(num, lang=lang_code, to = 'currency',)# currency='USD')
        else:
            words = num2words(num, lang=lang_code, to = 'currency', currency='USD')
            words = words.replace('dollars', 'rials')
            words = words.replace('cents', 'halalas')
            words = words.replace('billion', '')
        return words

    #  <span t-esc="o.amount_to_text_custom(o.amount_total, 'ar')"/>
