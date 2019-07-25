# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PersonOffAssociateToAddressOff(models.TransientModel):
    _description = 'Person (Off) Associate to Address (Off)'
    _name = 'clv.person_off.associate_to_address_off'

    def _default_person_off_ids(self):
        return self._context.get('active_ids')
    person_off_ids = fields.Many2many(
        comodel_name='clv.person_off',
        relation='clv_person_off_associate_to_address_off_rel',
        string='Persons (Off)',
        default=_default_person_off_ids
    )

    create_new_address_off = fields.Boolean(
        string='Create new Address (Off)',
        default=True,
        readonly=True
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
    def do_person_off_associate_to_address_off(self):
        self.ensure_one()

        person_off_count = 0
        for person_off in self.person_off_ids:

            person_off_count += 1

            _logger.info(u'%s %s %s', '>>>>>', person_off_count, person_off.name)

            AddressOff = self.env['clv.address_off']
            address_off = AddressOff.search([
                ('related_address_id', '=', person_off.ref_address_id.id),
            ])
            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'address_off_id:', address_off.id)

            if address_off.id is not False:

                new_address_off = address_off

            else:

                if self.create_new_address_off:

                    values = {}
                    values['street'] = person_off.ref_address_id.street

                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                    new_address_off = AddressOff.create(values)
                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'new_address_off:', new_address_off)

                    values = {}
                    values['related_address_id'] = person_off.ref_address_id.id
                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                    new_address_off.write(values)

                    new_address_off.do_address_off_get_related_address_data()

            data_values = {}
            data_values['ref_address_off_id'] = new_address_off.id
            _logger.info(u'>>>>>>>>>> %s', data_values)
            person_off.write(data_values)

        if person_off_count == 1:

            action = {
                'type': 'ir.actions.act_window',
                'name': 'Addresses (Off)',
                'res_model': 'clv.address_off',
                'res_id': new_address_off.id,
                'view_type': 'form',
                'view_mode': 'tree,kanban,form',
                'target': 'current',
                'context': {'search_default_name': new_address_off.name},
            }

        else:

            action = {
                'type': 'ir.actions.act_window',
                'name': 'Addresses (Off)',
                'res_model': 'clv.address_off',
                'view_type': 'form',
                'view_mode': 'tree,kanban,form',
                'target': 'current',
            }

        return action
        # return True
