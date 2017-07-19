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

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PersonUpdate(models.TransientModel):
    _inherit = 'clv.person.updt'

    global_marker_id = fields.Many2one(
        comodel_name='clv.global_marker',
        string='Global Marker'
    )
    global_marker_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Global Marker', default=False, readonly=False, required=False
    )

    @api.multi
    def do_person_updt(self):
        self.ensure_one()

        super(PersonUpdate, self).do_person_updt()

        for person in self.person_ids:

            _logger.info(u'%s %s', '>>>>>', person.name)

            if self.global_marker_id_selection == 'set':
                person.global_marker_id = self.global_marker_id
            if self.global_marker_id_selection == 'remove':
                person.global_marker_id = False

        return True
