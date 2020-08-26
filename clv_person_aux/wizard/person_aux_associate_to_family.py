# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PersonAuxAssociateToFamily(models.TransientModel):
    _description = 'Person (Aux) Associate to Family'
    _name = 'clv.person_aux.associate_to_family'

    def _default_person_aux_ids(self):
        return self._context.get('active_ids')
    person_aux_ids = fields.Many2many(
        comodel_name='clv.person_aux',
        relation='clv_person_aux_associate_to_family_rel',
        string='Persons (Aux)',
        default=_default_person_aux_ids
    )

    create_new_family = fields.Boolean(string='Create new Family', default=False)
    associate_all_persons_from_ref_address = fields.Boolean(
        string='Associate all Persons from Reference Address',
        default=False
    )

    family_verification_exec = fields.Boolean(
        string='Family Verification Execute',
        default=True,
    )

    person_aux_verification_exec = fields.Boolean(
        string='Person (Aux) Verification Execute',
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

    def do_person_aux_associate_to_family(self):
        self.ensure_one()

        person_aux_count = 0
        for person_aux in self.person_aux_ids:

            person_aux_count += 1

            _logger.info(u'%s %s %s', '>>>>>', person_aux_count, person_aux.name)

            Family = self.env['clv.family']
            family = False

            if person_aux.ref_address_id.id is not False:
                family = Family.search([
                    ('ref_address_id', '=', person_aux.ref_address_id.id),
                ])

                if len(family) < 2:

                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'family_id:', family.id)

                    if family.id is not False:

                        data_values = {}
                        data_values['family_id'] = family.id
                        _logger.info(u'>>>>>>>>>> %s', data_values)
                        person_aux.write(data_values)
                        person_aux.related_person_id.write(data_values)

                    else:

                        if self.create_new_family:

                            values = {}
                            values['name'] = person_aux.ref_address_id.name

                            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                            new_family = Family.create(values)
                            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'new_family:', new_family)

                            values = {}
                            values['code'] = '/'
                            values['phase_id'] = person_aux.phase_id.id
                            values['street_name'] = person_aux.ref_address_id.street_name
                            values['street2'] = person_aux.ref_address_id.street2
                            values['country_id'] = person_aux.ref_address_id.country_id.id
                            values['state_id'] = person_aux.ref_address_id.state_id.id
                            values['city'] = person_aux.ref_address_id.city
                            values['zip'] = person_aux.ref_address_id.zip
                            # values['phone'] = person_aux.ref_address_id.phone
                            # values['mobile'] = person_aux.ref_address_id.mobile
                            # values['email'] = person_aux.ref_address_id.email

                            values['street_number'] = person_aux.ref_address_id.street_number
                            values['district'] = person_aux.ref_address_id.district
                            values['city_id'] = person_aux.ref_address_id.city_id.id

                            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                            new_family.write(values)

                            values = {}
                            values['ref_address_id'] = person_aux.ref_address_id.id
                            values['reg_state'] = 'revised'
                            values['state'] = person_aux.ref_address_id.state
                            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                            new_family.write(values)

                            values = {}
                            values['family_id'] = new_family.id
                            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                            person_aux.write(values)
                            person_aux.related_person_id.write(values)

                            if self.associate_all_persons_from_ref_address:

                                Person = self.env['clv.person']
                                persons = Person.search([
                                    ('ref_address_id', '=', person_aux.ref_address_id.id),
                                ])

                                for other_person in persons:

                                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'other_person:', other_person)
                                    values = {}
                                    values['family_id'] = new_family.id
                                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                                    other_person.write(values)

            if self.family_verification_exec:
                if person_aux.family_id.id is not False:
                    person_aux.family_id._family_verification_exec()

            if self.person_aux_verification_exec:
                if person_aux.related_person_id.id is not False:
                    person_aux.related_person_id._person_verification_exec()
                person_aux._person_aux_verification_exec()

        # return action
        return True
