# -*- coding: utf-8 -*-


from __future__ import division, print_function, unicode_literals
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from pybrasil.inscricao import (formata_cnpj, formata_cpf, limpa_formatacao, formata_inscricao_estadual, valida_cnpj, valida_cpf, valida_inscricao_estadual)
from pybrasil.telefone import (formata_fone, valida_fone_fixo, valida_fone_celular, valida_fone_internacional, valida_fone, formata_varios_fones)
from pybrasil.base import mascara, primeira_maiuscula
#from integra_rh.models.hr_employee import SEXO, ESTADO_CIVIL
from email_validator import validate_email, EmailNotValidError
from ..constante_tributaria import *


IE_DESTINATARIO = (
    ('1', 'Contribuinte'),
    ('2', 'Isento'),
    ('9', 'Não contribuinte/estrangeiro'),
)


TIPO_PESSOA = (
    ('F', 'Física'),
    ('J', 'Jurídica'),
    ('E', 'Estrangeiro'),
    ('I', 'Indeterminado'),
)


class Partner(models.Model):
    _description = 'Participantes'
    #_name = 'cadastro.participante'
    #_inherit = ['mail.thread']
    _name = 'res.partner'
    _inherit = 'res.partner'
    _rec_name = 'nome'
    _order = 'nome, cnpj_cpf'

    codigo = fields.Char(string='Código', size=60, index=True)
    nome = fields.Char(string='Nome', size=60, index=True)

    eh_orgao_publico = fields.Boolean('É órgão público?')
    eh_cooperativa = fields.Boolean('É cooperativa?')
    eh_sindicato = fields.Boolean('É sindicato?')
    eh_consumidor_final = fields.Boolean('É consumidor final?')
    #eh_sociedade = fields.Boolean('É sociedade?')
    eh_convenio = fields.Boolean('É convênio?')
    eh_cliente = fields.Boolean('É cliente?')
    eh_fornecedor = fields.Boolean('É fornecedor?')
    eh_transportadora = fields.Boolean('É transportadora?')

    #empresa_ids = fields.One2many('res.company', 'partner_id', 'Empresa/unidade')
    #usuario_ids = fields.One2many('res.users', 'partner_id', 'Usuário')
    eh_grupo = fields.Boolean('É grupo?', index=True)
    eh_empresa = fields.Boolean('É empresa?', index=True)
    eh_usuario = fields.Boolean('É usuário?', index=True)
    eh_funcionario = fields.Boolean('É funcionário?')

    cnpj_cpf = fields.Char('CNPJ/CPF', size=18,  help='Para participantes estrangeiros, usar EX9999, onde 9999 é um número a sua escolha', index=True)
    tipo_pessoa = fields.Char('Tipo pessoa', size=1, compute='_tipo_pessoa', store=True, index=True)

    @api.one
    @api.depends('cnpj_cpf')
    def _tipo_pessoa(self):
        self.tipo_pessoa = 'I'

        if self.cnpj_cpf:
            if self.cnpj_cpf[:2] == 'EX':
                self.tipo_pessoa = 'E'
                self.contribuinte = INDICADOR_IE_DESTINATARIO_NAO_CONTRIBUINTE

            elif len(self.cnpj_cpf) == 18:
                self.tipo_pessoa = 'J'
                self.contribuinte = INDICADOR_IE_DESTINATARIO_ISENTO

            else:
                self.tipo_pessoa = 'F'
                self.contribuinte = INDICADOR_IE_DESTINATARIO_NAO_CONTRIBUINTE

    razao_social = fields.Char('Razão Social', size=60, index=True)
    fantasia = fields.Char('Fantasia', size=60, index=True)
    endereco = fields.Char('Endereço', size=60)
    numero = fields.Char('Número', size=60)
    complemento = fields.Char('Complemento', size=60)
    bairro = fields.Char('Bairro', size=60)
    municipio_id = fields.Many2one('sped.municipio', string='Município', ondelete='restrict')
    cidade = fields.Char('Município', related='municipio_id.nome', store=True, index=True)
    estado = fields.UpperChar('Estado', related='municipio_id.estado', store=True, index=True)
    cep = fields.Char('CEP', size=9)
    #
    # Telefone e email para a emissão da NF-e
    #
    fone = fields.Char('Fone', size=18)
    fone_comercial = fields.Char('Fone Comercial', size=18)
    celular = fields.Char('Celular', size=18)
    email = fields.Email('Email', size=60)
    site = fields.Site('Site', size=60)
    email_nfe = fields.Email('Email para envio da NF-e', size=60)
    #
    # Inscrições e registros
    #
    contribuinte = fields.Selection(IE_DESTINATARIO, string='Contribuinte', default='2')
    ie = fields.Char('Inscrição estadual', size=18)
    im = fields.Char('Inscrição municipal', size=14)
    suframa = fields.Char('SUFRAMA', size=12)
    rntrc = fields.Char('RNTRC', size=15)
    cnae_id = fields.Many2one('sped.cnae', 'CNAE principal')
    cei = fields.Char('CEI', size=15)

    rg_numero = fields.Char('RG', size=14)
    rg_orgao_emissor = fields.UpperChar('Órgão emisssor do RG', size=20)
    rg_data_expedicao = fields.Date('Data de expedição do RG')
    crc = fields.Char('Conselho Regional de Contabilidade', size=14)
    crc_uf = fields.Many2one('sped.estado', string='UF do CRC', ondelete='restrict')
    profissao = fields.Char('Cargo', size=40)
    #'sexo = fields.selection(SEXO, 'Sexo' )
    #'estado_civil = fields.selection(ESTADO_CIVIL, 'Estado civil')
    pais_nacionalidade_id = fields.Many2one('sped.pais', string='Nacionalidade', ondelete='restrict')

    #
    # Campos para o RH
    #
    codigo_sindical = fields.Char('Código sindical', size=30)
    codigo_ans = fields.Char('Código ANS', size=6)

    #
    # Para a contabilidade
    #
    #sociedade_ids = fields.One2many('res.partner.sociedade', 'partner_id', 'Sociedade')

    #
    # Endereços e contatos
    #
    #address_ids = fields.One2many('res.partner.address', 'partner_id', 'Contatos e endereços')

    #
    # Para o faturamento
    #
    transportadora_id = fields.Many2one('res.partner', string='Transportadora', ondelete='restrict')
    regime_tributario = fields.Selection(REGIME_TRIBUTARIO, string='Regime tributário', default=REGIME_TRIBUTARIO_SIMPLES, index=True)

    #@api.depends('nome', 'razao_social', 'fantasia', 'cnpj_cpf')
    #def name_get(self, cr, uid, ids, context={}):
        #if not len(ids):
            #return []

        #res = []
        #for partner_obj in self.browse(cr, uid, ids):
            #if hasattr(partner_obj, 'nome'):
                #nome = partner_obj.nome or ''

                #if partner_obj.cnpj_cpf:
                    #nome += ' - ' + partner_obj.cnpj_cpf

                #if partner_obj.razao_social and partner_obj.razao_social.upper() != partner_obj.nome.upper():
                    #nome += ' [' + partner_obj.razao_social + ']'

                #if partner_obj.fantasia and partner_obj.fantasia.upper() != partner_obj.nome.upper():
                    #if partner_obj.razao_social:
                        #if partner_obj.razao_social.upper() != partner_obj.fantasia.upper():
                            #nome += ' [' + partner_obj.fantasia + ']'

                    #else:
                        #nome += ' [' + partner_obj.fantasia + ']'

                #res.append((partner_obj.id, nome))
            #else:
                #res.append((partner_obj.id, ''))

        #return res

    @api.model
    def name_search(self, name='', args=[], operator='ilike', limit=100):
        if name and operator in ('=', 'ilike', '=ilike', 'like'):
            if operator != '=':
                name = name.strip().replace(' ', '%')

            args += [
                '|',
                ('codigo', '=', name),
                '|',
                ('razao_social', 'ilike', name),
                '|',
                ('fantasia', 'ilike', name),
                '|',
                ('cnpj_cpf', 'ilike', mascara(name, '  .   .   /    -  ')),
                ('cnpj_cpf', 'ilike', mascara(name, '   .   .   -  ')),
            ]

        return super(Partner, self).name_search(name=name, args=args, operator=operator, limit=limit)

    @api.model
    def create(self, dados):
        if 'razao_social' in dados and not dados['razao_social']:
            dados['razao_social'] = dados['nome']

        dados['name'] = dados['nome']

        partner = super(Partner, self).create(dados)

        #print('criou partner', dados)
        #print(partner.eh_empresa)

        if partner.eh_empresa or partner.eh_grupo:
            company = self.env['res.company'].sudo().create({
                'name': partner.nome,
                'partner_id': partner.id,
                'currency_id': 1,
            })

            partner.write({'company_id': company.id})

        return partner

    @api.multi
    def write(self, dados):
        if 'nome' in dados:
            dados['name'] = dados['nome']

        res = super(Partner, self).write(dados)

        if 'nome' in dados:
            for partner in self:
                if partner.eh_empresa:
                    partner.company_id.write({'name': partner.nome})

        return res

    def _valida_cnpj_cpf(self):
        valores = {}
        res = {'value': valores}

        if not self.cnpj_cpf:
            return res

        cnpj_cpf = limpa_formatacao(self.cnpj_cpf or '')

        if cnpj_cpf[:2] != 'EX':
            if not valida_cnpj(cnpj_cpf) and not valida_cpf(cnpj_cpf):
                raise ValidationError('CNPJ/CPF inválido')

        if len(cnpj_cpf) == 14:
            valores['cnpj_cpf'] = formata_cnpj(cnpj_cpf)
            valores['tipo_pessoa'] = 'J'
            valores['regime_tributario'] = '1'
        else:
            valores['cnpj_cpf'] = formata_cpf(cnpj_cpf)
            valores['tipo_pessoa'] = 'F'
            valores['regime_tributario'] = '3'

        if cnpj_cpf[:2] == 'EX':
            valores['tipo_pessoa'] = 'E'
            valores['regime_tributario'] = '3'

        if self.id:
            cnpj_ids = self.search([('cnpj_cpf', '=', cnpj_cpf), ('id', '!=', self.id), ('eh_empresa', '=', False), ('eh_grupo', '=', False)])
        else:
            cnpj_ids = self.search([('cnpj_cpf', '=', cnpj_cpf), ('eh_empresa', '=', False), ('eh_grupo', '=', False)])

        if len(cnpj_ids) > 0:
            raise ValidationError('CNPJ/CPF já existe no cadastro!')

        return res

    @api.one
    @api.constrains('cnpj_cpf')
    def constrains_cnpj_cpf(self):
        self._valida_cnpj_cpf()

    @api.onchange('cnpj_cpf')
    def onchange_cnpj_cpf(self):
        return self._valida_cnpj_cpf()

    def _valida_fone(self):
        valores = {}
        res = {'value': valores}

        if self.fone:
            if (not valida_fone_internacional(self.fone)) and (not valida_fone_fixo(self.fone)):
                raise ValidationError('Telefone fixo inválido!')

            valores['fone'] = formata_fone(self.fone)

        if self.fone_comercial:
            if (not valida_fone_internacional(self.fone_comercial)) and (not valida_fone_fixo(self.fone_comercial)) and (not valida_fone_celular(self.fone_comercial)):
                raise ValidationError('Telefone comercial inválido!')

            valores['fone_comercial'] = formata_fone(self.fone_comercial)

        if self.celular:
            if (not valida_fone_internacional(self.celular)) and (not valida_fone_celular(self.celular)):
                raise ValidationError('Celular inválido!')

            valores['celular'] = formata_fone(self.celular)

        return res

    @api.one
    @api.constrains('fone', 'celular', 'fone_comercial')
    def constrains_fone(self):
        self._valida_fone()

    @api.onchange('fone', 'celular', 'fone_comercial')
    def onchange_fone(self):
        return self._valida_fone()

    def _valida_cep(self):
        valores = {}
        res = {'value': valores}

        if not self.cep:
            return res

        cep = limpa_formatacao(self.cep)
        if (not cep.isdigit()) or len(cep) != 8:
            raise ValidationError('CEP inválido!')

        valores['cep'] = cep[:5] + '-' + cep[5:]

        return res

    @api.one
    @api.constrains('cep')
    def constrains_cep(self):
        self._valida_cep()

    @api.onchange('cep')
    def onchange_cep(self):
        return self._valida_cep()

    def _valida_ie(self):
        valores = {}
        res = {'value': valores}

        if self.suframa:
            if not valida_inscricao_estadual(suframa, 'SUFRAMA'):
                raise ValidationError('Inscrição na SUFRAMA inválida!')

            valores['suframa'] = formata_inscricao_estadual(self.suframa, 'SUFRAMA')

        if self.ie:
            if self.contribuinte == '2' or self.contribuinte == '3':
                valores['ie'] = ''

            else:
                if not self.municipio_id:
                    raise ValidationError('Para validação da inscrição estadual é preciso informar o município!')

                if self.ie.strip().upper()[:6] == 'ISENTO' or self.ie.strip().upper()[:6] == 'ISENTA':
                    raise ValidationError('Inscrição estadual inválida para contribuinte!')

                if not valida_inscricao_estadual(self.ie, self.municipio_id.estado_id.uf):
                    raise ValidationError('Inscrição estadual inválida!')

                valores['ie'] = formata_inscricao_estadual(self.ie, self.municipio_id.estado_id.uf)

        return res

    @api.one
    @api.constrains('suframa', 'ie', 'municipio_id', 'contribuinte')
    def constrains_ie(self):
        self._valida_ie()

    @api.onchange('suframa', 'ie', 'municipio_id', 'contribuinte')
    def onchange_ie(self):
        return self._valida_ie()

    def _valida_email(self):
        valores = {}
        res = {'value': valores}

        if self.email:
            email = self.email
            emails_validos = []

            if ',' not in email:
                email = self.email + ','

            for e in email.split(','):
                if e.strip() == '':
                    continue

                try:
                    valido = validate_email(e.strip())
                    emails_validos.append(valido['email'])
                except:
                    raise ValidationError('Email %s inválido!' % e.strip())

            valores['email'] = ','.join(emails_validos)

        if self.email_nfe:
            email = self.email_nfe
            emails_validos = []

            if ',' not in email:
                email = self.email + ','

            for e in email.split(','):
                if e.strip() == '':
                    continue

                try:
                    valido = validate_email(e.strip())
                    emails_validos.append(valido['email'])
                except:
                    raise ValidationError('Email %s inválido!' % e.strip())

            valores['email_nfe'] = ','.join(emails_validos)

        return res

    @api.one
    @api.constrains('email', 'email_nfe')
    def constrains_email(self):
        self._valida_email()

    @api.onchange('email', 'email_nfe')
    def onchange_email(self):
        return self._valida_email()

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        if (not view_id) and (view_type == 'form') and self._context.get('force_email'):
            view_id = self.env.ref('sped.cadastro_participante_cliente_form').id
        res = super(Partner, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            res['arch'] = self.fields_view_get_address(res['arch'])
        return res

    @api.onchange('municipio_id')
    def onchange_municipio_id(self):
        res = {}
        valores = {}
        res['value'] = valores

        if self.municipio_id and self.municipio_id.cep_unico:
            valores['cep'] = self.municipio_id.cep_unico

        return res

    @api.onchange('nome', 'razao_social', 'fantasia', 'endereco', 'bairro', 'cidade', 'profissao')
    def onchange_nome(self):
        res = {}
        valores = {}
        res['value'] = valores

        if self.nome:
            valores['nome'] = primeira_maiuscula(self.nome)

        if self.razao_social:
            valores['razao_social'] = primeira_maiuscula(self.razao_social)

        if self.fantasia:
            valores['fantasia'] = primeira_maiuscula(self.fantasia)

        if self.endereco:
            valores['endereco'] = primeira_maiuscula(self.endereco)

        if self.bairro:
            valores['bairro'] = primeira_maiuscula(self.bairro)

        if self.cidade:
            valores['cidade'] = primeira_maiuscula(self.cidade)

        if self.profissao:
            valores['profissao'] = primeira_maiuscula(self.profissao)

        return res