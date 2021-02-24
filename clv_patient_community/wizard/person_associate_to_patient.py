# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PersonAssociateToPatient(models.TransientModel):
    _description = 'Person Associate to Patient'
    _name = 'clv.person.associate_to_patient'

    def _default_person_ids(self):
        return self._context.get('active_ids')
    person_ids = fields.Many2many(
        comodel_name='clv.person',
        relation='clv_person_associate_to_patient_rel',
        string='Persons',
        default=_default_person_ids
    )

    create_new_patient = fields.Boolean(
        string='Create new Patient',
        default=True,
        readonly=False
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

    def do_person_associate_to_patient(self):
        self.ensure_one()

        person_count = 0
        for person in self.person_ids:

            person_count += 1

            _logger.info(u'%s %s %s', '>>>>>', person_count, person.name)

            Patient = self.env['clv.patient']
            patient = Patient.search([
                ('related_person_id', '=', person.id),
            ])
            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'patient_id:', patient.id)

            if patient.id is not False:

                new_patient = patient

            else:

                if self.create_new_patient:

                    values = {}
                    values['name'] = person.name
                    values['street_name'] = person.street_name

                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                    new_patient = Patient.create(values)
                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'new_patient:', new_patient)

                    values = {}
                    values['related_person_id'] = person.id
                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                    new_patient.write(values)

                    new_patient.do_patient_get_related_person_data()

        if person_count == 1:

            action = {
                'type': 'ir.actions.act_window',
                'name': 'Patients',
                'res_model': 'clv.patient',
                'res_id': new_patient.id,
                'view_type': 'form',
                'view_mode': 'tree,kanban,form',
                'target': 'current',
                'context': {'search_default_name': new_patient.name},
            }

        else:

            action = {
                'type': 'ir.actions.act_window',
                'name': 'Patients',
                'res_model': 'clv.patient',
                'view_type': 'form',
                'view_mode': 'tree,kanban,form',
                'target': 'current',
            }

        return action
        # return True
