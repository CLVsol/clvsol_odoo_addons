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


class DocumentItemEdit(models.TransientModel):
    _name = 'clv.document.item_edit'

    def _get_default(self, document_type_id_code, item_code):
        active_id = self.env['clv.document'].browse(self._context.get('active_id'))
        if active_id.document_type_id.code == document_type_id_code:
            value = active_id.item_ids.search([
                ('document_id', '=', active_id.id),
                ('code', '=', item_code),
            ]).value
        else:
            value = False
        return value

    def _set_value(self, document_type_id_code, item_code, value):
        active_id = self.env['clv.document'].browse(self._context.get('active_id'))
        if active_id.document_type_id.code == document_type_id_code:
            item_reg = active_id.item_ids.search([
                ('document_id', '=', active_id.id),
                ('code', '=', item_code),
            ])
            item_reg.value = value

    def _default_document_id(self):
        return self._context.get('active_id')
    document_id = fields.Many2one(
        comodel_name='clv.document',
        string='Document',
        readonly=True,
        default=_default_document_id
    )

    def _default_document_type_id(self):
        return self.env['clv.document'].browse(self._context.get('active_id')).document_type_id
    document_type_id = fields.Many2one(
        comodel_name='clv.document.type',
        string='Document Type',
        readonly=True,
        default=_default_document_type_id
    )

    @api.multi
    def _reopen_form(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
        return action

    @api.multi
    def do_document_updt(self):
        self.ensure_one()

        document = self.env['clv.document'].browse(self._context.get('active_id'))

        _logger.info(u'%s %s', '>>>>>', document.code)

        return True
