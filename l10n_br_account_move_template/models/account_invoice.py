# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Daniel Sadamo - KMEE INFORMATICA
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp import api, models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _map_move_template_domain(self, move_line, line_type):
        """
        Método para mapear qual é o roteiro correto para cada tipo de
        lançamento ou manter as contas originais caso não exista roteiro que
        se encaixe na operação
        :param move_line:
        :param line_type:
        :return:
        """
        values_dict = {'type': line_type}
        domain = ['&']
        invl = self.env['account.invoice.line'].browse(move_line.get('invl_id',
                                                                     False))
        duration = fields.Datetime.from_string(self.date_due) + \
                                               relativedelta(years=-1)
        if duration > datetime.today():
            term = 'longo'
        else:
            term = 'curto'
        if invl:
            product = invl.product_id
            values_dict.update(dict(
                operation_destination=invl.cfop_id.id_dest or False,
                product_fiscal_type=product.type or False,
                product_origin=product.origin or False,
            ))
        if line_type == 'tax':
            values_dict.update(dict(
                debit_account_id=move_line['account_id'] or False
            ))
        values_dict.update(dict(
            company_id=self.company_id.id or False,
            fiscal_document_id=self.fiscal_document_id.id or False,
            fiscal_category=self.fiscal_category_id.id or False,
            operation_type=self.fiscal_category_id.type or False,
            term=term,
        ))

        for key, value in values_dict.iteritems():
            domain.append('|')
            domain.append((key, '=', value))
            domain.append((key, '=', False))

        return domain

    def define_account(self, move_line, line_type):
        """
        Definir contas das novas partidas de acordo com o roteiro contabil
        :param move_line:  - dict - partida duplicada para contra-partida
                                    na conta contabil
        :param line_type: sting - Tipo de partida
                                    ['CLIENTE', 'RECEITA', 'IMPOSTO']
        :return:
        """
        account_id = False
        amt = self.env['account.move.template']
        domain = self._map_move_template_domain(move_line, line_type)
        amt = amt.search(domain)
        if line_type == 'receipt':

            if move_line['debit']:
                account_id = amt.debit_account_id
            else:
                account_id = amt.credit_account_id

        elif line_type == 'tax':
            account_id = amt.debit_account_id

        # Se definir uma conta no mapeamento, seta a conta,
        # senão fica com a conta padrão
        if account_id:
            move_line['account_id'] = account_id

    def finalize_invoice_move_lines(self, move_lines):
        """
        Sobrescrever hook do core para criar as contrapartidas de acordo com
        o tipo da partida e mapear as contas seguindo o roteiro contábil.
        :param move_lines: lista com [0,0, dict] - Move lines geradas pelo core
        :return: - lista com [0,0, dict] onde o dict são as partidas a serem
                                        criadas para o lançamento contabil
                                        da invoice.
        """
        move_lines = super(AccountInvoice, self).finalize_invoice_move_lines(
            move_lines)
        lines = list(move_lines)
        for move in lines:
            if move[2].get('product_id', False):
                line_type = 'receipt'
                # move_lines.remove(move)

            elif move[2].get('tax_amount', False):
                line_type = 'tax'

            else:
                line_type = 'client'

            # Criar contra-partidas
            if line_type in ['tax', 'receipt']:
                partida = dict(move[2])
                partida['name'] = 'Contrapartida - ' + move[2]['name']
                partida['debit'] = move[2]['credit']
                partida['credit'] = move[2]['debit']
                move_lines.append([0, 0, partida])
                self.define_account(move[2], line_type)

        return move_lines

    def line_get_convert(self, line, part, date):
        res = super(AccountInvoice, self).line_get_convert(line, part, date)
        res.update(dict(
            invl_id=line.get('invl_id', False)
        ))
        return res


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.model
    def move_line_get_item(self, line):
        res = super(AccountInvoiceLine, self).move_line_get_item(line)
        res.update(dict(
            invl_id=line.id
        ))
        return res
