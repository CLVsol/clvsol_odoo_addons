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

from datetime import *

from odoo import api, fields, models


class PersonHistory(models.Model):
    _description = 'Person History'
    _name = 'clv.person.history'
    _order = "sign_in_date desc"

    person_id = fields.Many2one(
        comodel_name='clv.person',
        string='Person',
        required=False
    )
    sign_in_date = fields.Date(
        string='Sign in date',
        required=False,
        default=lambda *a: datetime.now().strftime('%Y-%m-%d')
    )
    sign_out_date = fields.Date(
        string="Sign out date",
        required=False
    )

    category_ids = fields.Many2many(
        comodel_name='clv.person.category',
        relation='clv_person_category_person_history_rel',
        column1='person_history_id',
        column2='category_id',
        string='Categories'
    )
    category_names = fields.Char(
        string='Category Names',
        compute='_compute_category_names',
        store=True
    )
    category_names_suport = fields.Char(
        string='Category Names Suport',
        compute='_compute_category_names_suport',
        store=False
    )

    date_reference = fields.Date(string="Reference Date")
    age_reference = fields.Char(string='Reference Age')

    responsible_id = fields.Many2one(
        comodel_name='clv.person',
        string='Responsible',
        ondelete='restrict'
    )
    caregiver_id = fields.Many2one(
        comodel_name='clv.person',
        string='Caregiver',
        ondelete='restrict'
    )

    address_id = fields.Many2one(
        comodel_name='clv.address',
        string='Address',
        ondelete='restrict'
    )
    person_address_role_id = fields.Many2one(
        comodel_name='clv.person.address.role',
        string='Person Address Role',
        required=False
    )

    notes = fields.Text(string='Notes')

    active = fields.Boolean(string='Active', default=1)

    @api.depends('category_ids')
    def _compute_category_names(self):
        for r in self:
            r.category_names = r.category_names_suport

    @api.multi
    def _compute_category_names_suport(self):
        for r in self:
            category_names = False
            for category in r.category_ids:
                if category_names is False:
                    category_names = category.complete_name
                else:
                    category_names = category_names + ', ' + category.complete_name
            r.category_names_suport = category_names
            if r.category_names != category_names:
                record = self.env['clv.person'].search([('id', '=', r.id)])
                record.write({'category_ids': r.category_ids})


class Person(models.Model):
    _inherit = 'clv.person'

    person_history_ids = fields.One2many(
        comodel_name='clv.person.history',
        inverse_name='person_id',
        string='Person History'
    )
