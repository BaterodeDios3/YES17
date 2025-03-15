# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _, Command
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_round, float_repr, float_compare


class BiPosSession(models.Model):
    _inherit = 'pos.session'
    

    custom_analytic_id = fields.Many2one('account.analytic.account', string="Custom Analytic")

    def _create_combine_account_payment(self, payment_method, amounts, diff_amount):
        outstanding_account = payment_method.outstanding_account_id or self.company_id.account_journal_payment_debit_account_id
        destination_account = self._get_receivable_account(payment_method)

        if float_compare(amounts['amount'], 0, precision_rounding=self.currency_id.rounding) < 0:
            # revert the accounts because account.payment doesn't accept negative amount.
            outstanding_account, destination_account = destination_account, outstanding_account

        account_payment = self.env['account.payment'].create({
            'amount': abs(amounts['amount']),
            'journal_id': payment_method.journal_id.id,
            'force_outstanding_account_id': outstanding_account.id,
            'destination_account_id': destination_account.id,
            'ref': _('Combine %s POS payments from %s') % (payment_method.name, self.name),
            'pos_payment_method_id': payment_method.id,
            'pos_session_id': self.id,
            'custom_analytic_id': self.custom_analytic_id.id if self.custom_analytic_id else False,
        })

        diff_amount_compare_to_zero = self.currency_id.compare_amounts(diff_amount, 0)
        if diff_amount_compare_to_zero != 0:
            self._apply_diff_on_account_payment_move(account_payment, payment_method, diff_amount)

        account_payment.action_post()
        return account_payment.move_id.line_ids.filtered(
            lambda line: line.account_id == account_payment.destination_account_id)

    def _create_split_account_payment(self, payment, amounts):
        payment_method = payment.payment_method_id
        if not payment_method.journal_id:
            return self.env['account.move.line']
        outstanding_account = payment_method.outstanding_account_id or self.company_id.account_journal_payment_debit_account_id
        accounting_partner = self.env["res.partner"]._find_accounting_partner(payment.partner_id)
        destination_account = accounting_partner.property_account_receivable_id

        if float_compare(amounts['amount'], 0, precision_rounding=self.currency_id.rounding) < 0:
            # revert the accounts because account.payment doesn't accept negative amount.
            outstanding_account, destination_account = destination_account, outstanding_account

        account_payment = self.env['account.payment'].create({
            'amount': abs(amounts['amount']),
            'partner_id': payment.partner_id.id,
            'journal_id': payment_method.journal_id.id,
            'force_outstanding_account_id': outstanding_account.id,
            'destination_account_id': destination_account.id,
            'ref': _('%s POS payment of %s in %s') % (payment_method.name, payment.partner_id.display_name, self.name),
            'pos_payment_method_id': payment_method.id,
            'pos_session_id': self.id,
            'custom_analytic_id': self.custom_analytic_id.id if self.custom_analytic_id else False,
        })
        account_payment.action_post()
        return account_payment.move_id.line_ids.filtered(
            lambda line: line.account_id == account_payment.destination_account_id)

    def _create_diff_account_move_for_split_payment_method(self, payment_method, diff_amount):
        self.ensure_one()

        get_diff_vals_result = self._get_diff_vals(payment_method.id, diff_amount)
        if not get_diff_vals_result:
            return

        source_vals, dest_vals = get_diff_vals_result
        diff_move = self.env['account.move'].create({
            'journal_id': payment_method.journal_id.id,
            'date': fields.Date.context_today(self),
            'ref': self._get_diff_account_move_ref(payment_method),
            'line_ids': [Command.create(source_vals), Command.create(dest_vals)],
            'custom_analytic_id': self.custom_analytic_id.id if self.custom_analytic_id else False,
        })
        diff_move._post()

    def _create_cash_statement_lines_and_cash_move_lines(self, data):
        data = super(BiPosSession, self)._create_cash_statement_lines_and_cash_move_lines(data)
        if self.custom_analytic_id:
            if data.get('split_cash_statement_lines', False):
                data.get('split_cash_statement_lines').write({
                    'custom_analytic_id': self.custom_analytic_id.id,
                })

            if data.get('split_cash_receivable_lines', False):
                data.get('split_cash_receivable_lines').write({
                    'custom_analytic_id': self.custom_analytic_id.id,
                    'analytic_distribution': {self.custom_analytic_id.id: 100}
                })

            if data.get('combine_cash_statement_lines', False):
                data.get('combine_cash_statement_lines').write({
                    'custom_analytic_id': self.custom_analytic_id.id,
                })

            if data.get('combine_cash_receivable_lines', False):
                data.get('combine_cash_receivable_lines').write({
                    'custom_analytic_id': self.custom_analytic_id.id,
                    'analytic_distribution': {self.custom_analytic_id.id: 100}
                })

        return data

    def _debit_amounts(self, partial_move_line_vals, amount, amount_converted, force_company_currency=False):
        data = super(BiPosSession, self)._debit_amounts(partial_move_line_vals, amount, amount_converted,
                                                        force_company_currency=force_company_currency)
        if self.custom_analytic_id:
            data.update({
                'custom_analytic_id': self.custom_analytic_id.id,
                'analytic_distribution': {self.custom_analytic_id.id: 100}
            })

        return data

    def _credit_amounts(self, partial_move_line_vals, amount, amount_converted, force_company_currency=False):
        data = super(BiPosSession, self)._credit_amounts(partial_move_line_vals, amount, amount_converted,
                                                         force_company_currency=force_company_currency)
        if self.custom_analytic_id:
            data.update({
                'custom_analytic_id': self.custom_analytic_id.id,
                'analytic_distribution': {self.custom_analytic_id.id: 100}
            })

        return data

    def close_session_from_ui(self, bank_payment_method_diff_pairs=None):

        bank_payment_method_diffs = dict(bank_payment_method_diff_pairs or [])
        self.ensure_one()

        check_closing_session = self._cannot_close_session(bank_payment_method_diffs)
        if check_closing_session:
            return check_closing_session

        validate_result = self.action_pos_session_closing_control(bank_payment_method_diffs=bank_payment_method_diffs)

        if isinstance(validate_result, dict):
            return {
                'successful': False,
                'message': validate_result.get('name'),
                'redirect': True
            }

        self.message_post(body='Point of Sale Session ended')

        return {'successful': True}

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        result += [
            'pos.order'
        ]
        return result

    def _loader_params_pos_order(self):
        return {
            'search_params': {
                'fields': [
                    'custom_analytic_id',
                ],
            }
        }

    def _get_pos_ui_pos_order(self, params):
        return self.env['pos.order'].search_read(**params['search_params'])

    def _loader_params_pos_payment_method(self):
        result = super()._loader_params_pos_payment_method()
        result['search_params']['fields'].extend(['custom_analytic_id'])
        return result

    def _loader_params_pos_session(self):
        result = super()._loader_params_pos_session()
        result['search_params']['fields'].extend(['custom_analytic_id'])
        return result


class BiPosOrder(models.Model):
    _inherit = 'pos.order'

    custom_analytic_id = fields.Many2one('account.analytic.account', related='session_id.custom_analytic_id',
                                         string="Custom Analytic", readonly=True)

    def _prepare_invoice_line(self, order_line):
        res = super(BiPosOrder, self)._prepare_invoice_line(order_line)
        if self.custom_analytic_id:
            res.update({
                'custom_analytic_id': self.custom_analytic_id.id,
                'analytic_distribution': {self.custom_analytic_id.id: 100}
            })
        return res

    def _prepare_invoice_vals(self):
        res = super(BiPosOrder, self)._prepare_invoice_vals()
        res.update({
            'custom_analytic_id': self.custom_analytic_id.id,
        })
        return res

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(BiPosOrder, self)._order_fields(ui_order)
        order_fields['custom_analytic_id'] = ui_order.get('custom_analytic_id', False)
        return order_fields

    @api.model
    def _payment_fields(self, order, ui_paymentline):
        res = super(BiPosOrder, self)._payment_fields(order, ui_paymentline)
        res['custom_analytic_id'] = ui_paymentline.get('custom_analytic_id', False)
        return res


class BiPosPayment(models.Model):
    _inherit = 'pos.payment'

    custom_analytic_id = fields.Many2one('account.analytic.account', related='session_id.custom_analytic_id',
                                         string="Custom Analytic")

    def _create_payment_moves(self, is_reverse=False):
        result = self.env['account.move']
        for payment in self:
            order = payment.pos_order_id
            payment_method = payment.payment_method_id
            if payment_method.type == 'pay_later' or float_is_zero(payment.amount,
                                                                   precision_rounding=order.currency_id.rounding):
                continue
            accounting_partner = self.env["res.partner"]._find_accounting_partner(payment.partner_id)
            pos_session = order.session_id
            journal = pos_session.config_id.journal_id
            payment_move = self.env['account.move'].with_context(default_journal_id=journal.id).create({
                'journal_id': journal.id,
                'date': fields.Date.context_today(order, order.date_order),
                'ref': _('Invoice payment for %s (%s) using %s') % (
                order.name, order.account_move.name, payment_method.name),
                'pos_payment_ids': payment.ids,
                'custom_analytic_id': self.custom_analytic_id.id if self.custom_analytic_id else False,
            })
            result |= payment_move
            payment.write({'account_move_id': payment_move.id})
            amounts = pos_session._update_amounts({'amount': 0, 'amount_converted': 0}, {'amount': payment.amount},
                                                  payment.payment_date)
            credit_line_vals = pos_session._credit_amounts({
                'account_id': accounting_partner.with_company(order.company_id).property_account_receivable_id.id,
                # The field being company dependant, we need to make sure the right value is received.
                'partner_id': accounting_partner.id,
                'move_id': payment_move.id,
            }, amounts['amount'], amounts['amount_converted'])
            is_split_transaction = payment.payment_method_id.split_transactions
            if is_split_transaction and is_reverse:
                reversed_move_receivable_account_id = accounting_partner.with_company(order.company_id).property_account_receivable_id.id
            elif is_reverse:
                reversed_move_receivable_account_id = payment.payment_method_id.receivable_account_id.id or self.company_id.account_default_pos_receivable_account_id.id
            else:
                reversed_move_receivable_account_id = self.company_id.account_default_pos_receivable_account_id.id
            debit_line_vals = pos_session._debit_amounts({
                'account_id': reversed_move_receivable_account_id,
                'move_id': payment_move.id,
                'partner_id': accounting_partner.id if is_split_transaction and is_reverse else False,
            }, amounts['amount'], amounts['amount_converted'])
        
            if self.custom_analytic_id:
                credit_line_vals.update({
                    'custom_analytic_id': self.custom_analytic_id.id,
                    'analytic_distribution': {self.custom_analytic_id.id: 100}
                })
                debit_line_vals.update({
                    'custom_analytic_id': self.custom_analytic_id.id,
                    'analytic_distribution': {self.custom_analytic_id.id: 100}
                })

            self.env['account.move.line'].create([credit_line_vals, debit_line_vals])
            payment_move._post()
        return result


class BiPosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    custom_analytic_id = fields.Many2one('account.analytic.account', string="Custom Analytic")


class pos_analytic_account_bank_statement_line(models.Model):
    _inherit = 'account.bank.statement.line'

    custom_analytic_id = fields.Many2one('account.analytic.account', related='pos_session_id.custom_analytic_id')

    def _prepare_move_line_default_vals(self, counterpart_account_id=None):
        """ Prepare the dictionary to create the default account.move.lines for the current account.bank.statement.line
        record.
        :return: A list of python dictionary to be passed to the account.move.line's 'create' method.
        """
        self.ensure_one()

        if not counterpart_account_id:
            counterpart_account_id = self.journal_id.suspense_account_id.id

        if not counterpart_account_id:
            raise UserError(_(
                "You can't create a new statement line without a suspense account set on the %s journal.",
                self.journal_id.display_name,
            ))

        company_currency = self.journal_id.company_id.currency_id
        journal_currency = self.journal_id.currency_id or company_currency
        foreign_currency = self.foreign_currency_id or journal_currency or company_currency

        journal_amount = self.amount
        if foreign_currency == journal_currency:
            transaction_amount = journal_amount
        else:
            transaction_amount = self.amount_currency
        if journal_currency == company_currency:
            company_amount = journal_amount
        elif foreign_currency == company_currency:
            company_amount = transaction_amount
        else:
            company_amount = journal_currency \
                ._convert(journal_amount, company_currency, self.journal_id.company_id, self.date)

        liquidity_line_vals = {
            'name': self.payment_ref,
            'move_id': self.move_id.id,
            'partner_id': self.partner_id.id,
            'account_id': self.journal_id.default_account_id.id,
            'currency_id': journal_currency.id,
            'amount_currency': journal_amount,
            'debit': company_amount > 0 and company_amount or 0.0,
            'credit': company_amount < 0 and -company_amount or 0.0,
        }

        # Create the counterpart line values.
        counterpart_line_vals = {
            'name': self.payment_ref,
            'account_id': counterpart_account_id,
            'move_id': self.move_id.id,
            'partner_id': self.partner_id.id,
            'currency_id': foreign_currency.id,
            'amount_currency': -transaction_amount,
            'debit': -company_amount if company_amount < 0.0 else 0.0,
            'credit': company_amount if company_amount > 0.0 else 0.0,
        }
        return [liquidity_line_vals, counterpart_line_vals]


class account_payment(models.Model):
    _inherit = 'account.payment'

    custom_analytic_id = fields.Many2one('account.analytic.account', string="Analytic Account on POS Order")

    @api.model_create_multi
    def create(self, vals_list):
        result = super(account_payment, self).create(vals_list)

        if result:
            for vals in vals_list:
                if vals.get('communication'):
                    pos = self.env['pos.session'].search(['|', ('name', '=', vals.get('communication')),
                                                          ('name', '=ilike', vals.get('communication'))])
                    if pos:
                        if pos.custom_analytic_id:
                            result.update({
                                'custom_analytic_id': pos.custom_analytic_id.id
                            })
        return result


class AccountMove(models.Model):
    _inherit = 'account.move'

    custom_analytic_id = fields.Many2one('account.analytic.account', string="Analytic Account on POS Order")

    @api.model_create_multi
    def create(self, vals_list):
        rec = super(AccountMove, self).create(vals_list)
        if rec:
            for vals in vals_list:
                if vals.get('origin') or vals.get('ref'):
                    session_name = vals.get('origin') or vals.get('ref')
                    pos = self.env['pos.session'].sudo().search([('name', '=', session_name)])
                    if pos:
                        if pos.custom_analytic_id:
                            rec.update({
                                'custom_analytic_id': pos.custom_analytic_id.id,
                            })
        return rec


class account_payment_line(models.Model):
    _inherit = 'account.move.line'

    custom_analytic_id = fields.Many2one('account.analytic.account', string="Analytic Account",
                                         related='move_id.custom_analytic_id')
