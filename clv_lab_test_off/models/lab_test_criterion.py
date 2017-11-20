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
    _inherit = "clv.lab_test.criterion"

    lab_test_off_report_id = fields.Many2one(comodel_name='clv.lab_test.off.report', string='Test Report')

    _sql_constraints = [
        ('report_off_code_uniq',
         'UNIQUE(lab_test_off_report_id, code)',
         u'Error! The Code must be unique for a Test Report Off!'
         ),
    ]


class LabTestOffReport(models.Model):
    _inherit = 'clv.lab_test.off.report'

    criterion_ids = fields.One2many(
        comodel_name='clv.lab_test.criterion',
        inverse_name='lab_test_off_report_id',
        string='Test Cases'
    )
