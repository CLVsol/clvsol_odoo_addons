# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AddressAuxSetCode(models.TransientModel):
    _description = 'Address (Aux) Set Code'
    _name = 'clv.address_aux.set_code'

    def _default_address_aux_ids(self):
        return self._context.get('active_ids')
    address_aux_ids = fields.Many2many(
        comodel_name='clv.address_aux',
        relation='clv_address_aux_set_code_rel',
        string='Addresses (Aux)',
        default=_default_address_aux_ids
    )

    address_aux_verification_exec = fields.Boolean(
        string='Address (Aux) Verification Execute',
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

    # @api.model
    # def default_get(self, field_names):

    #     defaults = super().default_get(field_names)

    #     defaults['address_aux_ids'] = self.env.context['active_ids']

    #     return defaults

    def do_address_aux_set_code(self):
        self.ensure_one()

        for address_aux in self.address_aux_ids:

            _logger.info(u'%s %s', '>>>>>', address_aux.name)

            address_aux._address_aux_set_code()

            if self.address_aux_verification_exec:
                address_aux._address_aux_verification_exec()

        return True
