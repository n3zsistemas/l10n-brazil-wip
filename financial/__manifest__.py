# -*- coding: utf-8 -*-
# Copyright 2017 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Financial',
    'summary': """
        Financial""",
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'KMEE,Odoo Community Association (OCA)',
    'website': 'www.kmee.com.br',
    'depends': [
        'l10n_br_resource',
        'account_payment_mode',
        'account',
        'mail',
    ],
    'data': [

        'security/account_account_type.xml',
        'security/financial_move.xml',
        'security/res_partner_bank.xml',
        'views/financial_menu.xml',

        'data/ir_sequence_data.xml',
        'data/financial_move_data.xml',

        'wizards/financial_cancel.xml',
        'wizards/financial_edit.xml',
        'wizards/financial_create.xml',
        'wizards/financial_pay_receive.xml',

        'views/account_account_type.xml',
        'views/financial_move_base_view.xml',
        'views/payment_mode.xml',
        'views/inherited_res_partner_bank_view.xml',

        'report/financial_cashflow.xml',
        'report/financial_statement_report.xml',
        'report/report_financial.xml',
    ],
    'demo': [
        'demo/financial_move.xml',
        'demo/financial_demo.yml'
    ],
}