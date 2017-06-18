# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import fields, models


class LabTestTypeCriterion(models.Model):
    _description = 'Lab Test Criterion'
    _name = "clv.lab_test.criterion"
    _order = "sequence"

    code = fields.Char(string='Criterion Code')
    name = fields.Char(string='Test')

    # result = fields.Text('Results')
    result = fields.Char(sring='Results')
    unit_id = fields.Many2one(comodel_name='clv.lab_test.unit', string='Unit')
    normal_range = fields.Text(string='Normal Range')

    lab_test_type_id = fields.Many2one(comodel_name='clv.lab_test.type', string='Test Type')

    lab_test_result_id = fields.Many2one(comodel_name='clv.lab_test.result', string='Test Result')

    sequence = fields.Integer(
        string='Sequence',
        default=10
    )

    active = fields.Boolean(string='Active', default=1)

    # _sql_constraints = [
    #     ('code_uniq',
    #      'UNIQUE(code)',
    #      u'Error! The Code must be unique!'
    #      )
    # ]


class LabTestType(models.Model):
    _inherit = 'clv.lab_test.type'

    criterion_ids = fields.One2many(
        comodel_name='clv.lab_test.criterion',
        inverse_name='lab_test_type_id',
        string='Test Cases'
    )


class LabTestResult(models.Model):
    _inherit = 'clv.lab_test.result'

    criterion_ids = fields.One2many(
        comodel_name='clv.lab_test.criterion',
        inverse_name='lab_test_result_id',
        string='Test Cases'
    )
