# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LabTestTypeParameter(models.Model):
    _description = 'Lab Test Type  '
    _name = "clv.lab_test.type.parameter"
    _order = "name, criterion_code"

    name = fields.Char(string='Parameter', required=True)
    criterion_code = fields.Char(string='Criterion Code', required=True)

    criterion_type = fields.Char(string='Criterion Type', required=True)

    lab_test_type_id = fields.Many2one(
        comodel_name='clv.lab_test.type',
        string='Lab Test Type',
        required=False)

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('parameter_uniq',
         'UNIQUE(lab_test_type_id, name, criterion_code)',
         u'Error! The pair (Parameter, Criterion Code) must be unique for a Lab Test Type!'
         ),
    ]


class LabTestType(models.Model):
    _inherit = 'clv.lab_test.type'

    parameter_ids = fields.One2many(
        comodel_name='clv.lab_test.type.parameter',
        inverse_name='lab_test_type_id',
        string='Parameters'
    )
