# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo import exceptions


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'
    _order = 'title'

    code = fields.Char(string='Survey Code', required=False)

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Survey Code must be unique!'),
    ]

    def copy(self):
        raise exceptions.ValidationError('It is not possible to duplicate the record, please create a new one.')
