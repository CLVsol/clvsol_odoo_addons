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


class PersonOffLog(models.Model):
    _description = 'Person Off Log'
    _name = 'clv.person.off.log'
    _inherit = 'clv.object.log'

    person_off_id = fields.Many2one(
        comodel_name='clv.person.off',
        string='Person Off',
        required=True,
        ondelete='cascade'
    )


class PersonOff(models.Model):
    _name = "clv.person.off"
    _inherit = 'clv.person.off', 'clv.log.model'

    log_ids = fields.One2many(
        comodel_name='clv.person.off.log',
        inverse_name='person_off_id',
        string='Person Log',
        readonly=True
    )

    @api.one
    def insert_object_log(self, person_off_id, values, action, notes):
        if self.active_log or 'active_log' in values:
            if str(values).find("'category_ids': clv.person.off.category(") == -1:
                vals = {
                    'person_off_id': person_off_id,
                    'values': values,
                    'action': action,
                    'notes': notes,
                }
                self.env['clv.person.off.log'].create(vals)
