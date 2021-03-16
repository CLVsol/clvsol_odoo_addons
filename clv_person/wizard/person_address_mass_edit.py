# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PersonAddressMassEdit(models.TransientModel):
    _description = 'Person Address Mass Edit'
    _name = 'clv.person.address_mass_edit'

    def _default_person_ids(self):
        return self._context.get('active_ids')
    person_ids = fields.Many2many(
        comodel_name='clv.person',
        relation='clv_person_address_mass_edit_rel',
        string='Persons',
        default=_default_person_ids
    )

    marker_ids = fields.Many2many(
        comodel_name='clv.address.marker',
        relation='clv_person_address_mass_edit_marker_rel',
        column1='person_id',
        column2='address_marker_id',
        string='Address Markers'
    )
    marker_ids_selection = fields.Selection(
        [('add', 'Add'),
         ('remove_m2m', 'Remove'),
         ('set', 'Set'),
         ], string='Address Markers:', default=False, readonly=False, required=False
    )

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

    def do_person_address_mass_edit(self):
        self.ensure_one()

        for person in self.person_ids:

            _logger.info(u'%s %s', '>>>>>', person)

            Address = self.env['clv.address']
            address = Address.with_context({'active_test': False}).search([
                ('id', '=', person.ref_address_id.id),
            ])

            _logger.info(u'%s %s', '>>>>>>>>>>', address.name)

            if address.id is not False:

                if self.marker_ids_selection == 'add':
                    m2m_list = []
                    for address_marker_id in self.marker_ids:
                        m2m_list.append((4, address_marker_id.id))
                    _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                    address.marker_ids = m2m_list
                if self.marker_ids_selection == 'remove_m2m':
                    m2m_list = []
                    for address_marker_id in self.marker_ids:
                        m2m_list.append((3, address_marker_id.id))
                    _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                    address.marker_ids = m2m_list
                if self.marker_ids_selection == 'set':
                    m2m_list = []
                    for address_marker_id in address.marker_ids:
                        m2m_list.append((3, address_marker_id.id))
                    _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                    address.marker_ids = m2m_list
                    m2m_list = []
                    for address_marker_id in self.marker_ids:
                        m2m_list.append((4, address_marker_id.id))
                    _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                    address.marker_ids = m2m_list

        return True
