# -*- coding: utf-8 -*-
#
# Copyright 2017 Taŭga Tecnologia
#   Aristides Caldeira <aristides.caldeira@tauga.com.br>
# License AGPL-3 or later (http://www.gnu.org/licenses/agpl)
#

from __future__ import division, print_function, unicode_literals


NATUREZA_CONTA_CONTABIL = (
    ('01', 'Ativo'),
    ('02', 'Passivo'),
    ('03', 'Patrimônio líquido'),
    ('04', 'Resultado'),
    ('05', 'Compensação'),
    ('09', 'Outras'),
)
NATUREZA_CONTA_CONTABIL_ATIVO = '01'
NATUREZA_CONTA_CONTABIL_PASSIVO = '02'
NATUREZA_CONTA_CONTABIL_PATRIMONIO = '03'
NATUREZA_CONTA_CONTABIL_RESULTADO = '04'
NATUREZA_CONTA_CONTABIL_COMPENSACAO = '05'
NATUREZA_CONTA_CONTABIL_OUTRAS = '09'


TIPO_SPED_CONTA_CONTABIL = (
    ('S', 'Sintética'),
    ('A', 'Analítica'),
)
TIPO_SPED_CONTA_CONTABIL_SINTETICA = 'S'
TIPO_SPED_CONTA_CONTABIL_ANALITICA = 'A'


TIPO_CONTA_CONTABIL = (
    ('ativo', 'Ativo'),  # natureza 01
    ('caixa', 'Caixa e bancos'),  # natureza 01
    ('receber', 'A receber'),  # natureza 01
    ('passivo', 'Passivo'),  # natureza 02
    ('receita', 'Receita'),  # natureza 09
    ('despesa', 'Despesa'),  # natureza 09
    ('custo', 'Custo'),  # natureza 09
    ('pagar', 'A pagar'),  # natureza 02
    ('resultado', 'Resultado'),  # natureza 04
    ('compensacao', 'Compensação'),  # natureza 05
    ('patrimonio', 'Patrimônio líquido'),  # natureza 03
    ('outras', 'Outras'),  # natureza 09
)
TIPO_CONTA_CONTABIL_ATIVO = 'ativo'
TIPO_CONTA_CONTABIL_CAIXA = 'caixa'
TIPO_CONTA_CONTABIL_RECEBER = 'receber'
TIPO_CONTA_CONTABIL_PASSIVO = 'passivo'
TIPO_CONTA_CONTABIL_RECEITA = 'receita'
TIPO_CONTA_CONTABIL_DESPESA = 'despesa'
TIPO_CONTA_CONTABIL_CUSTO = 'custo'
TIPO_CONTA_CONTABIL_PAGAR = 'pagar'
TIPO_CONTA_CONTABIL_RESULTADO = 'resultado'
TIPO_CONTA_CONTABIL_COMPENSACAO = 'compensacao'
TIPO_CONTA_CONTABIL_PATRIMONIO = 'patrimonio'
TIPO_CONTA_CONTABIL_OUTRAS = 'outras'

TIPO_CONTA_CONTABIL_NATUREZA = {
    TIPO_CONTA_CONTABIL_ATIVO: NATUREZA_CONTA_CONTABIL_ATIVO,
    TIPO_CONTA_CONTABIL_CAIXA: NATUREZA_CONTA_CONTABIL_ATIVO,
    TIPO_CONTA_CONTABIL_RECEBER: NATUREZA_CONTA_CONTABIL_ATIVO,
    TIPO_CONTA_CONTABIL_PASSIVO: NATUREZA_CONTA_CONTABIL_PASSIVO,
    TIPO_CONTA_CONTABIL_RECEITA: NATUREZA_CONTA_CONTABIL_OUTRAS,
    TIPO_CONTA_CONTABIL_DESPESA: NATUREZA_CONTA_CONTABIL_OUTRAS,
    TIPO_CONTA_CONTABIL_CUSTO: NATUREZA_CONTA_CONTABIL_OUTRAS,
    TIPO_CONTA_CONTABIL_PAGAR: NATUREZA_CONTA_CONTABIL_PASSIVO,
    TIPO_CONTA_CONTABIL_RESULTADO: NATUREZA_CONTA_CONTABIL_RESULTADO,
    TIPO_CONTA_CONTABIL_COMPENSACAO: NATUREZA_CONTA_CONTABIL_COMPENSACAO,
    TIPO_CONTA_CONTABIL_PATRIMONIO: NATUREZA_CONTA_CONTABIL_PATRIMONIO,
    TIPO_CONTA_CONTABIL_OUTRAS: NATUREZA_CONTA_CONTABIL_OUTRAS,
}
