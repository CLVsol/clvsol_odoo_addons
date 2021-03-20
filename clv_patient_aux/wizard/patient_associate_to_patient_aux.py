# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatientAssociateToPatientAux(models.TransientModel):
    _description = 'Patient Associate to Patient (Aux)'
    _name = 'clv.patient.associate_to_patient_aux'

    def _default_patient_ids(self):
        return self._context.get('active_ids')
    patient_ids = fields.Many2many(
        comodel_name='clv.patient',
        relation='clv_patient_associate_to_patient_aux_rel',
        string='Patients',
        default=_default_patient_ids
    )

    create_new_patient_aux = fields.Boolean(
        string='Create new Patient (Aux)',
        default=True,
        readonly=False
    )

    patient_verification_exec = fields.Boolean(
        string='Patient Verification Execute',
        default=True,
    )

    patient_aux_verification_exec = fields.Boolean(
        string='Patient (Aux) Verification Execute',
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

    def do_patient_associate_to_patient_aux(self):
        self.ensure_one()

        patient_count = 0
        for patient in self.patient_ids:

            patient_count += 1

            _logger.info(u'%s %s %s', '>>>>>', patient_count, patient.name)

            PatientAux = self.env['clv.patient_aux']
            patient_aux = PatientAux.search([
                ('related_patient_id', '=', patient.id),
            ])
            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'patient_aux_id:', patient_aux.id)

            if patient_aux.id is not False:

                new_patient_aux = patient_aux

            else:

                if self.create_new_patient_aux:

                    values = {}
                    values['name'] = patient.name
                    values['street_name'] = patient.street_name

                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                    new_patient_aux = PatientAux.create(values)
                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'new_patient_aux:', new_patient_aux)

                    values = {}
                    values['related_patient_id'] = patient.id
                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                    new_patient_aux.write(values)

                    new_patient_aux.do_patient_aux_get_related_patient_data()

            if self.patient_verification_exec:
                patient._patient_verification_exec()

            if self.patient_aux_verification_exec:
                new_patient_aux._patient_aux_verification_exec()

        if patient_count == 1:

            action = {
                'type': 'ir.actions.act_window',
                'name': 'Patients (Aux)',
                'res_model': 'clv.patient_aux',
                'res_id': new_patient_aux.id,
                'view_type': 'form',
                'view_mode': 'tree,kanban,form',
                'target': 'current',
                'context': {'search_default_name': new_patient_aux.name},
            }

        else:

            action = {
                'type': 'ir.actions.act_window',
                'name': 'Patients (Aux)',
                'res_model': 'clv.patient_aux',
                'view_type': 'form',
                'view_mode': 'tree,kanban,form',
                'target': 'current',
            }

        return action
        # return True
