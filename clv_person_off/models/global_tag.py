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

from odoo import api, models, fields


class Tag(models.Model):
    _inherit = 'clv.global_tag'

    person_off_ids = fields.Many2many(
        comodel_name='clv.person.off',
        relation='clv_person_off_global_tag_rel',
        column1='global_tag_id',
        column2='person_off_id',
        string='Persons Off'
    )


class PersonOff(models.Model):
    _inherit = 'clv.person.off'

    global_tag_ids = fields.Many2many(
        comodel_name='clv.global_tag',
        relation='clv_person_off_global_tag_rel',
        column1='person_off_id',
        column2='global_tag_id',
        string='Global Tags'
    )
    global_tag_names = fields.Char(
        string='Global Tag Names',
        compute='_compute_global_tag_names',
        store=True
    )
    global_tag_names_suport = fields.Char(
        string='Global Tag Names Suport',
        compute='_compute_global_tag_names_suport',
        store=False
    )

    @api.depends('global_tag_ids')
    def _compute_global_tag_names(self):
        for r in self:
            r.global_tag_names = r.global_tag_names_suport

    @api.multi
    def _compute_global_tag_names_suport(self):
        for r in self:
            global_tag_names = False
            for global_tag in r.global_tag_ids:
                if global_tag_names is False:
                    global_tag_names = global_tag.complete_name
                else:
                    global_tag_names = global_tag_names + ', ' + global_tag.complete_name
            r.global_tag_names_suport = global_tag_names
            if r.global_tag_names != global_tag_names:
                record = self.env['clv.person.off'].search([('id', '=', r.id)])
                record.write({'global_tag_ids': r.global_tag_ids})
