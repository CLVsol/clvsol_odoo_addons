# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AddressAssociateToResidence(models.TransientModel):
    _description = 'Address Associate to Residence'
    _name = 'clv.address.associate_to_residence'

    def _default_address_ids(self):
        return self._context.get('active_ids')
    address_ids = fields.Many2many(
        comodel_name='clv.address',
        relation='clv_address_associate_to_residence_rel',
        string='Addresss',
        default=_default_address_ids
    )

    create_new_residence = fields.Boolean(
        string='Create new Residence',
        default=True,
        readonly=False
    )

    address_verification_exec = fields.Boolean(
        string='Address Verification Execute',
        default=True,
    )

    residence_verification_exec = fields.Boolean(
        string='Residence Verification Execute',
        default=True,
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

    def do_address_associate_to_residence(self):
        self.ensure_one()

        address_count = 0
        for address in self.address_ids:

            address_count += 1

            _logger.info(u'%s %s %s', '>>>>>', address_count, address.name)

            Residence = self.env['clv.residence']
            residence = Residence.search([
                ('related_address_id', '=', address.id),
            ])
            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'residence_id:', residence.id)

            if residence.id is not False:

                new_residence = residence

            else:

                if self.create_new_residence:

                    values = {}
                    values['name'] = address.name
                    values['street_name'] = address.street_name

                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                    new_residence = Residence.create(values)
                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'new_residence:', new_residence)

                    values = {}
                    values['related_address_id'] = address.id
                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                    new_residence.write(values)

                    new_residence.do_residence_get_related_address_data()

            if self.address_verification_exec:
                address._address_verification_exec()

            if self.residence_verification_exec:
                new_residence._residence_verification_exec()

        if address_count == 1:

            action = {
                'type': 'ir.actions.act_window',
                'name': 'Residences',
                'res_model': 'clv.residence',
                'res_id': new_residence.id,
                'view_type': 'form',
                'view_mode': 'tree,kanban,form',
                'target': 'current',
                'context': {'search_default_name': new_residence.name},
            }

        else:

            action = {
                'type': 'ir.actions.act_window',
                'name': 'Residences',
                'res_model': 'clv.residence',
                'view_type': 'form',
                'view_mode': 'tree,kanban,form',
                'target': 'current',
            }

        return action
        # return True
