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


class DocumentMassEdit(models.TransientModel):
    _inherit = 'clv.document.mass_edit'

    phase_id = fields.Many2one(
        comodel_name='clv.phase',
        string='Phase'
    )
    phase_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Phase', default=False, readonly=False, required=False
    )

    @api.multi
    def do_document_mass_edit(self):
        self.ensure_one()

        super(DocumentMassEdit, self).do_document_mass_edit()

        for document in self.document_ids:

            _logger.info(u'%s %s', '>>>>>', document.name)

            if self.phase_id_selection == 'set':
                document.phase_id = self.phase_id
            if self.phase_id_selection == 'remove':
                document.phase_id = False

        return True
