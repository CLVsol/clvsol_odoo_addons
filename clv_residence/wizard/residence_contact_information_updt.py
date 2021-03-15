# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResidenceContactInformationUpdate(models.TransientModel):
    _description = 'Residence Contact Information Update'
    _name = 'clv.residence.contact_information_updt'

    def _default_residence_ids(self):
        return self._context.get('active_ids')
    residence_ids = fields.Many2many(
        comodel_name='clv.residence',
        relation='clv_residence_contact_information_updt_rel',
        string='Residences',
        default=_default_residence_ids
    )

    updt_phone = fields.Boolean(string='Update Phone', default=False)
    updt_mobile = fields.Boolean(string='Update Mobile', default=False)
    updt_email = fields.Boolean(string='Update Email', default=False)

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

    def do_residence_contact_information_updt(self):
        self.ensure_one()

        residence_count = 0
        for residence in self.residence_ids:

            residence_count += 1

            _logger.info(u'%s %s %s', '>>>>>', residence_count, residence.name)

            if residence.ref_address_id is not False:

                values = {}

                values['street_name'] = residence.ref_address_id.street_name
                values['street2'] = residence.ref_address_id.street2
                values['country_id'] = residence.ref_address_id.country_id.id
                values['state_id'] = residence.ref_address_id.state_id.id
                values['city'] = residence.ref_address_id.city
                values['zip'] = residence.ref_address_id.zip
                if self.updt_phone:
                    values['phone'] = residence.ref_address_id.phone
                if self.updt_mobile:
                    values['mobile'] = residence.ref_address_id.mobile
                if self.updt_email:
                    values['email'] = residence.ref_address_id.email

                _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)

                residence.write(values)

        return True
