# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from datetime import date, timedelta
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model_create_multi
    def create(self, vals_list):
            res = super().create(vals_list)
            if any('date' in vals and vals.get('date') > str(fields.date.today()) for vals in vals_list):
                raise ValidationError(_("You can't create entry for date greater than today."))
            
            return res

    def action_post(self):
        if self.date > fields.date.today():
                raise ValidationError(_("You can't post the entry by date greater than today."))
        res = super().action_post()
        return res


    # def write(self, vals):
    #     if not vals:
    #         return True
    #     self._sanitize_vals(vals)
    #     for move in self:
    #         if (move.restrict_mode_hash_table and move.state == "posted" and set(vals).intersection(move._get_integrity_hash_fields())):
    #             raise UserError(_("You cannot edit the following fields due to restrict mode being activated on the journal: %s.") % ', '.join(move._get_integrity_hash_fields()))
    #         if (move.restrict_mode_hash_table and move.inalterable_hash and 'inalterable_hash' in vals) or (move.secure_sequence_number and 'secure_sequence_number' in vals):
    #             raise UserError(_('You cannot overwrite the values ensuring the inalterability of the accounting.'))
    #         if (move.posted_before and 'journal_id' in vals and move.journal_id.id != vals['journal_id']):
    #             raise UserError(_('You cannot edit the journal of an account move if it has been posted once.'))
    #         if (move.name and move.name != '/' and move.sequence_number not in (0, 1) and 'journal_id' in vals and move.journal_id.id != vals['journal_id'] and not move.quick_edit_mode):
    #             raise UserError(_('You cannot edit the journal of an account move if it already has a sequence number assigned.'))

    #         # You can't change the date or name of a move being inside a locked period.
    #         if move.state == "posted" and (
    #                 ('name' in vals and move.name != vals['name'])
    #                 or ('date' in vals and move.date != vals['date'])
    #         ):
    #             move._check_fiscalyear_lock_date()
    #             move.line_ids._check_tax_lock_date()

    #         # You can't post subtract a move to a locked period.
    #         if 'state' in vals and move.state == 'posted' and vals['state'] != 'posted':
    #             move._check_fiscalyear_lock_date()
    #             move.line_ids._check_tax_lock_date()

    #         if move.journal_id.sequence_override_regex and vals.get('name') and vals['name'] != '/' and not re.match(move.journal_id.sequence_override_regex, vals['name']):
    #             if not self.env.user.has_group('account.group_account_manager'):
    #                 raise UserError(_('The Journal Entry sequence is not conform to the current format. Only the Accountant can change it.'))
    #             move.journal_id.sequence_override_regex = False

    #     to_protect = []
    #     for fname in vals:
    #         field = self._fields[fname]
    #         if field.compute and not field.readonly:
    #             to_protect.append(field)
    #     stolen_moves = self.browse(set(move for move in self._stolen_move(vals)))
    #     container = {'records': self | stolen_moves}
    #     with self.env.protecting(to_protect, self), self._check_balanced(container):
    #         with self._sync_dynamic_lines(container):
    #             res = super(AccountMove, self.with_context(
    #                 skip_account_move_synchronization=True,
    #             )).write(vals)


    #             # Reset the name of draft moves when changing the journal.
    #             # Protected against holes in the pre-validation checks.
    #             if 'journal_id' in vals and 'name' not in vals:
    #                 self.name = False
    #                 self._compute_name()

    #             # You can't change the date of a not-locked move to a locked period.
    #             # You can't post a new journal entry inside a locked period.
    #             if 'date' in vals or 'state' in vals:
    #                 posted_move = self.filtered(lambda m: m.state == 'posted')
    #                 posted_move._check_fiscalyear_lock_date()
    #                 posted_move.line_ids._check_tax_lock_date()

    #             # Hash the move
    #             if vals.get('state') == 'posted':
    #                 self.flush_recordset()  # Ensure that the name is correctly computed before it is used to generate the hash
    #                 for move in self.filtered(lambda m: m.restrict_mode_hash_table and not(m.secure_sequence_number or m.inalterable_hash)).sorted(lambda m: (m.date, m.ref or '', m.id)):
    #                     new_number = move.journal_id.secure_sequence_id.next_by_id()
    #                     res |= super(AccountMove, move).write({
    #                         'secure_sequence_number': new_number,
    #                         'inalterable_hash': move._get_new_hash(new_number),
    #                     })

    #         self._synchronize_business_models(set(vals.keys()))

    #         # Apply the rounding on the Quick Edit mode only when adding a new line
    #         for move in self:
    #             if 'tax_totals' in vals:
    #                 super(AccountMove, move).write({'tax_totals': vals['tax_totals']})

    #     if 'journal_id' in vals:
    #         self.line_ids._check_constrains_account_id_journal_id()

    #     if self.date > fields.date.today():
    #             raise ValidationError(_("You can't modify the entry by date greater than today."))
    #     return res