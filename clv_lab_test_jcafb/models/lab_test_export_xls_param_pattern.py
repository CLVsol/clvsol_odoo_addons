# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LabTestTypeExportXlsParamPattern(models.Model):
    _description = 'Lab Test Export XLS Parameter Pattern'
    _name = "clv.lab_test.export_xls.param.pattern"

    display = fields.Selection(
        [('none', 'None'),
         ('result', 'Result'),
         ('report', 'Report')
         ], string='Display', default='none', readonly=False, required=True
    )

    parameter_type = fields.Selection(
        [('constant_char', 'Constant Char'),
         ('constant_int', 'Constant Integer'),
         ('constant_float', 'Constant Float'),
         ('image_file_name', 'Image File Name'),
         ('expression', 'Expression'),
         ('result_code', 'Result Code'),
         ('variable_name', 'Variable Name')
         ], string='Parameter Type', default='variable_name', readonly=False, required=True
    )

    parameter = fields.Char(string='Parameter')

    notes = fields.Text(string='Notes')

    active = fields.Boolean(string='Active', default=1)

    # _sql_constraints = [
    #     ('pattern_uniq',
    #      'UNIQUE(display, parameter_type, parameter)',
    #      u'Error! The Pattern must be unique!'
    #      ),
    # ]
