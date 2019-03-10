# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PersonOffContactInformationUpdate(models.TransientModel):
    _description = 'Person (Off) Contact Information Update'
    _name = 'clv.person_off.contact_information_updt'

    def _default_person_off_ids(self):
        return self._context.get('active_ids')
    person_off_ids = fields.Many2many(
        comodel_name='clv.person_off',
        relation='clv_person_off_contact_information_updt_rel',
        string='Persons (Off)',
        default=_default_person_off_ids
    )

    updt_phone = fields.Boolean(string='Update Phone', default=False)
    updt_mobile = fields.Boolean(string='Update Mobile', default=False)
    updt_email = fields.Boolean(string='Update Email', default=False)

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
    def do_person_off_contact_information_updt(self):
        self.ensure_one()

        for person_off in self.person_off_ids:

            _logger.info(u'%s %s', '>>>>>', person_off.name)

            if person_off.ref_address_id is not False:

                person_off.street = person_off.ref_address_id.street
                person_off.street2 = person_off.ref_address_id.street2
                person_off.country_id = person_off.ref_address_id.country_id
                person_off.state_id = person_off.ref_address_id.state_id
                person_off.city = person_off.ref_address_id.city
                person_off.zip = person_off.ref_address_id.zip
                if self.updt_phone:
                    person_off.phone = person_off.ref_address_id.phone
                if self.updt_mobile:
                    person_off.mobile = person_off.ref_address_id.mobile
                if self.updt_email:
                    person_off.email = person_off.ref_address_id.email

        return True
