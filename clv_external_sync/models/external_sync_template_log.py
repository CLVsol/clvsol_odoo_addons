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


class ExternalSyncTemplateLog(models.Model):
    _description = 'External Sync Template Log'
    _name = 'clv.external_sync.template.log'
    _inherit = 'clv.object.log'

    external_sync_template_id = fields.Many2one(
        comodel_name='clv.external_sync.template',
        string='External Sync Template',
        required=True,
        ondelete='cascade'
    )


class ExternalSyncTemplate(models.Model):
    _name = "clv.external_sync.template"
    _inherit = 'clv.external_sync.template', 'clv.log.model'

    log_ids = fields.One2many(
        comodel_name='clv.external_sync.template.log',
        inverse_name='external_sync_template_id',
        string='External Sync Template Log',
        readonly=True
    )

    @api.one
    def insert_object_log(self, external_sync_template_id, values, action, notes):
        if self.active_log or 'active_log' in values:
            vals = {
                'external_sync_template_id': external_sync_template_id,
                'values': values,
                'action': action,
                'notes': notes,
            }
            self.env['clv.external_sync.template.log'].create(vals)
