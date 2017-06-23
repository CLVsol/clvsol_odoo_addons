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

from odoo import api, fields, models


class InsuredAnnotationLog(models.Model):
    _description = 'Insured Annotation Log'
    _name = 'clv.insured.annotation.log'
    _inherit = 'clv.object.log'

    insured_annotation_id = fields.Many2one(
        comodel_name='clv.insured.annotation',
        string='Insured Annotation',
        required=True,
        ondelete='cascade'
    )


class InsuredAnnotation(models.Model):
    _name = "clv.insured.annotation"
    _inherit = 'clv.insured.annotation', 'clv.log.model'

    log_ids = fields.One2many(
        comodel_name='clv.insured.annotation.log',
        inverse_name='insured_annotation_id',
        string='Insured Annotation Log',
        readonly=True)

    @api.one
    def insert_object_log(self, insured_annotation_id, values, action, notes):
        if self.active_log or 'active_log' in values:
            vals = {
                'insured_annotation_id': insured_annotation_id,
                'values': values,
                'action': action,
                'notes': notes,
            }
            self.env['clv.insured.annotation.log'].create(vals)
