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

'''
Reference: http://help.openerp.com/question/18704/hide-menu-for-existing-group/

There are actually0-6 numbers for representing each job for a many2many/ one2many field

    (0, 0, { values }) -- link to a new record that needs to be created with the given values dictionary
    (1, ID, { values }) -- update the linked record with id = ID (write values on it)
    (2, ID) -- remove and delete the linked record with id = ID (calls unlink on ID, that will delete the
               object completely, and the link to it as well)
    (3, ID) -- cut the link to the linked record with id = ID (delete the relationship between the two
               objects but does not delete the target object itself)
    (4, ID) -- link to existing record with id = ID (adds a relationship)
    (5) -- unlink all (like using (3,ID) for all linked records)
    (6, 0, [IDs]) -- replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)
'''

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PersonAddressHistoryUpdate(models.TransientModel):
    _name = 'clv.person.address.history_updt'

    def _default_person_address_history_ids(self):
        return self._context.get('active_ids')
    person_address_history_ids = fields.Many2many(
        comodel_name='clv.person.address.history',
        relation='clv_person_address_history_updt_rel',
        string='Person Address History',
        default=_default_person_address_history_ids
    )

    global_tag_ids = fields.Many2many(
        comodel_name='clv.global_tag',
        relation='clv_person_adddress_history_updt_global_tag_rel',
        column1='person_address_history_id',
        column2='global_tag_id',
        string='Global Tags'
    )
    global_tag_ids_selection = fields.Selection(
        [('add', 'Add'),
         ('remove_m2m', 'Remove'),
         ('set', 'Set'),
         ], string='Global Tags', default=False, readonly=False, required=False
    )

    global_marker_id = fields.Many2one(
        comodel_name='clv.global_marker',
        string='Global Marker'
    )
    global_marker_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Global Marker', default=False, readonly=False, required=False
    )

    role_id = fields.Many2one(
        comodel_name='clv.person.address.role',
        string='Role'
    )
    role_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Role', default=False, readonly=False, required=False
    )

    sign_in_date = fields.Date(string='Sign in date', default=False, readonly=False, required=False)
    sign_in_date_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Sign in date', default=False, readonly=False, required=False
    )

    sign_out_date = fields.Date(string='Sign out date', default=False, readonly=False, required=False)
    sign_out_date_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Sign out date', default=False, readonly=False, required=False
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
    def do_person_address_history_updt(self):
        self.ensure_one()

        for person_address_history in self.person_address_history_ids:

            _logger.info(u'%s %s %%', '>>>>>',
                         person_address_history.person_id.name, person_address_history.address_id.name)

            if self.global_tag_ids_selection == 'add':
                m2m_list = []
                for global_tag_id in self.global_tag_ids:
                    m2m_list.append((4, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                person_address_history.global_tag_ids = m2m_list
            if self.global_tag_ids_selection == 'remove_m2m':
                m2m_list = []
                for global_tag_id in self.global_tag_ids:
                    m2m_list.append((3, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                person_address_history.global_tag_ids = m2m_list
            if self.global_tag_ids_selection == 'set':
                m2m_list = []
                for global_tag_id in person_address_history.global_tag_ids:
                    m2m_list.append((3, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                person_address_history.global_tag_ids = m2m_list
                m2m_list = []
                for global_tag_id in self.global_tag_ids:
                    m2m_list.append((4, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                person_address_history.global_tag_ids = m2m_list

            if self.global_marker_id_selection == 'set':
                _logger.info(u'%s %s', '>>>>>>>>>>', self.global_marker_id)
                person_address_history.global_marker_id = self.global_marker_id
            if self.global_marker_id_selection == 'remove':
                _logger.info(u'%s %s', '>>>>>>>>>>', False)
                person_address_history.global_marker_id = False

            if self.role_id_selection == 'set':
                person_address_history.role_id = self.role_id.id
            if self.role_id_selection == 'remove':
                person_address_history.role_id = False

            if self.sign_in_date_selection == 'set':
                person_address_history.sign_in_date = self.sign_in_date
            if self.sign_in_date_selection == 'remove':
                person_address_history.sign_in_date = False

            if self.sign_out_date_selection == 'set':
                person_address_history.sign_out_date = self.sign_out_date
            if self.sign_out_date_selection == 'remove':
                person_address_history.sign_out_date = False

        return True
