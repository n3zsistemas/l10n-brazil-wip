# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Daniel Sadamo - KMEE INFORMATICA
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models
from openerp.addons.l10n_br_account_product.models.product import \
    PRODUCT_ORIGIN

TERM = [
    ('curto', 'Curto prazo'),
    ('longo', 'Longo prazo')
]

OPERATION_DESTINATION = [
    ('1', u'Operação interna'),
    ('2', u'Operação interestadual'),
    ('3', u'Operação com exterior')
]

# OPERATION_PURPOSE = [
#     ('operacional', u'Operacional'),
#     ('financeiro', u'Financeiro'),
# ]

PRODUCT_TYPE = [
    ('product', u'Produto'),
    ('service', u'Serviço')
]

TYPE = [
    ('receipt', u'Receita'),
    ('tax', u'Imposto'),
    ('client', u'Cliente')
]


class AccountMoveTemplate(models.Model):
    _name = 'account.move.template'

    company_id = fields.Many2one(
        comodel_name='res.company',
    )
    type = fields.Selection(
        selection=TYPE,
        string=u'Tipo do lançamento'
    )
    fiscal_document_id = fields.Many2one(
        comodel_name='l10n_br_account.fiscal.document',
        string=u'Documento fiscal'
    )
    fiscal_category = fields.Many2one(
        comodel_name='l10n_br_account.fiscal.category',
        string=u'Categoria da operação'
    )
    operation_type = fields.Selection(
        related='fiscal_category.type',
        string=u'Tipo de operação'
    )
    operation_destination = fields.Selection(
        selection=OPERATION_DESTINATION,
        string=u'Destino da operação'
    )
    product_fiscal_type = fields.Selection(
        selection=PRODUCT_TYPE,
        string=u'Tipo fiscal do produto'
    )
    product_origin = fields.Selection(
        selection=PRODUCT_ORIGIN,
        string=u'Origem do produto'
    )
    term = fields.Selection(selection=TERM)
    # TODO: qual a melhor forma de estruturar?
    # operation_purpose = fields.Selection(selection=OPERATION_PURPOSE)
    # account_move_type = fields.Selection(selection=MOVE_TYPE)
    credit_account_id = fields.Many2one(
        comodel_name='account.account', string=u'Conta de credito'
    )
    debit_account_id = fields.Many2one(
        comodel_name='account.account', string=u'Conta de debito'
    )
    debit_compensation_account_id = fields.Many2one(
        comodel_name='account.account', string=u'Conta de compensaçao de '
                                               u'debito'
    )
    # ----------------------------------------------new fields----------

    # def _map_tax_domain(self, move_line):
    #     values_dict = {}
    #     domain = ['&']
    #     line = self.env['account.invoice.line'].browse(
    #         move_line.get('invl_id'))
    #     invoice =line.invoice_id
    #     term = 'curto'
    #     time = invoice.date_maturity - datetime.today()
    #     if time.years > 1:
    #         term = 'longo'
    #
    #     values_dict.update(
    #         dict(
    #             company_id=invoice.company_id.id,
    #             fiscal_document_id=invoice.fiscal_document_id.id,
    #             fiscal_category=invoice.fiscal_category_id.id,
    #             operation_destination=line.product_id.cfop.id_dest,
    #             product_fiscal_type=line.product.template.type,
    #             product_origin=line.product_id.origin,
    #             term=term,
    #             # credit_account_id=
    #
    #         )
    #     )
    #     for key, value in values_dict.iteritems():
    #         domain.append('|')
    #         domain.append((key, '=', value))
    #         domain.append((key, '=', False))
    #     return domain
    #
    # def _map_invoice_domain(self, move_line):
    #     values_dict = {}
    #     domain = ['&']
    #     line = self.env['account.invoice.line'].browse(
    #         move_line.get('invl_id'))
    #     invoice =line.invoice_id
    #     values_dict.update(
    #         dict(
    #             company_id=invoice.company_id.id,
    #             fiscal_document_id=invoice.fiscal_document_id.id,
    #             fiscal_category=invoice.fiscal_category_id.id,
    #             product_origin=line.product_id.origin,
    #             operation_destination=line.product_id.cfop.id_dest,
    #             product_fiscal_type=line.product.template.type,
    #         )
    #     )
    #     for key, value in values_dict.iteritems():
    #         domain.append('|')
    #         domain.append((key, '=', value))
    #         domain.append((key, '=', False))
    #
    #     # operation_nature
    #     # operation_position
    #     # product_type
    #     # term
    #     # account_move_type
    #     return domain
    #
    # def map_account(self, move_line):
    #     """ Parametros da tabela de decisão:
    #      - company_id, document_type_id,
    #                 account_type, operation_nature,
    #                 operation_position, product_type, product_origin, term,
    #                 operation_purpose, account_move_type
    #     :return: o objeto account.account
    #     """
    #     if move_line.get('invl_id'):
    #         domain = self._map_invoice_domain(move_line)
    #     elif move_line.get('tax_code'):
    #         domain = self._map_tax_domain(move_line)
    #     else:
    #         return move_line
    #
    #     rule = self.search(domain, limit=1)
    #
    #     # if rule:
    #         # move_line.update({'account_id': rule.debit_account_id.id or
    #                                          # rule.credit_account_id.id})
    #     return move_line
