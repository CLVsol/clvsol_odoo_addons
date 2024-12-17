# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


import re


def somaPoderada(numero):
    i = 0
    soma = 0
    while i < len(numero):
        soma = soma + int(numero[i]) * (15 - i)
        i = i + 1
    return soma


def validaCNS(numero):
    numero = str(numero)
    if numero.isdigit():
        if re.match(r'[1-2]\d{10}00[0-1]\d$', numero) or re.match(r'[7-9]\d{14}$', numero):
            return somaPoderada(numero) % 11 == 0
    return False


class Patient(models.Model):
    _name = "clv.patient"
    _inherit = 'clv.patient', 'clv.abstract.code'

    code = fields.Char(string='Patient Code', required=False, default='/')
    code_sequence = fields.Char(default='clv.person.code')

    @api.constrains('code')
    def _check_code(self):

        for record in self:

            if record.code is not False:

                sequence_str = ''
                for c in record.code:
                    if c.isdigit():
                        sequence_str = sequence_str + c
                sequence_str = sequence_str[:len(sequence_str) - 2]
                format_code = self.env['clv.abstract.code'].format_code(sequence_str)

                if record.code != format_code:
                    if not validaCNS(record.code):
                        raise UserError(u'Invalid Code!')
