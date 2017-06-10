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

from datetime import datetime

from odoo import fields, models


class LabTestRequest(models.Model):
    _description = 'Lab Test Request'
    _name = 'clv.lab_test.request'

    name = fields.Char(string="Lab Test Code")

    lab_test_type_id = fields.Many2one(
        comodel_name='clv.lab_test.type',
        string='Lab Test Type'
    )

    date_requested = fields.Datetime(
        string='Requested Date',
        default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    lab_test_result_id = fields.Many2one(
        comodel_name='clv.lab_test.result',
        string='Lab Test Result'
    )

    active = fields.Boolean(string='Active', default=1)


class LabTestType(models.Model):
    _inherit = 'clv.lab_test.type'

    lab_test_request_ids = fields.One2many(
        comodel_name='clv.lab_test.request',
        inverse_name='lab_test_type_id',
        string='Lab Test Requests'
    )
