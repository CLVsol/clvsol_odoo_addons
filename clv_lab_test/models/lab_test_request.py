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

from odoo import api, fields, models


class LabTestRequest(models.Model):
    _description = 'Lab Test Request'
    _name = 'clv.lab_test.request'
    _rec_name = 'code'
    _order = 'code'

    code = fields.Char(string="Lab Test Request Code")

    lab_test_type_ids = fields.Many2many(
        comodel_name='clv.lab_test.type',
        relation='clv_lab_test_request_lab_test_type_rel',
        column1='request_id',
        column2='type_id',
        string='Lab Test Types'
    )
    lab_test_type_names = fields.Char(
        string='Lab Test Type Names',
        compute='_compute_lab_test_type_names',
        store=True
    )
    lab_test_type_names_suport = fields.Char(
        string='Lab Test Type Names Suport',
        compute='_compute_lab_test_type_names_suport',
        store=False
    )

    date_requested = fields.Datetime(
        string='Requested Date',
        default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]

    @api.depends('lab_test_type_ids')
    def _compute_lab_test_type_names(self):
        for r in self:
            r.lab_test_type_names = r.lab_test_type_names_suport

    @api.multi
    def _compute_lab_test_type_names_suport(self):
        for r in self:
            lab_test_type_names = False
            for lab_test_type in r.lab_test_type_ids:
                if lab_test_type_names is False:
                    lab_test_type_names = lab_test_type.name
                else:
                    lab_test_type_names = lab_test_type_names + ', ' + lab_test_type.name
            r.lab_test_type_names_suport = lab_test_type_names
            if r.lab_test_type_names != lab_test_type_names:
                record = self.env['clv.lab_test.request'].search([('id', '=', r.id)])
                record.write({'lab_test_type_ids': r.lab_test_type_ids})


class LabTestType(models.Model):
    _inherit = 'clv.lab_test.type'

    lab_test_request_ids = fields.Many2many(
        comodel_name='clv.lab_test.request',
        relation='clv_lab_test_request_lab_test_type_rel',
        column1='type_id',
        column2='request_id',
        string='Lab Test Requests'
    )
