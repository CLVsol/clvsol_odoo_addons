# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models
from odoo import exceptions

_logger = logging.getLogger(__name__)


class PatientHistoryUpdate(models.TransientModel):
    _description = 'Patient History Update'
    _name = 'clv.patient.history_updt'

    def _default_patient_ids(self):
        return self._context.get('active_ids')
    patient_ids = fields.Many2many(
        comodel_name='clv.patient',
        relation='patient_history_updt_rel',
        string='Patients',
        default=_default_patient_ids
    )
    date_sign_in = fields.Date(
        string='Sign in date',
        required=False,
    )
    date_sign_out = fields.Date(
        string="Sign out date",
        required=False
    )

    # @api.multi
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

    # @api.multi
    def do_patient_history_updt(self):
        self.ensure_one()

        PatientHistory = self.env['clv.patient.history']

        for patient in self.patient_ids:

            if self.date_sign_out is False:
                raise exceptions.ValidationError('The "Sign out date" has not been defined!')
                return self._reopen_form()

            if self.date_sign_in is False:
                raise exceptions.ValidationError('The "Sign in date" has not been defined!')
                return self._reopen_form()

            _logger.info(u'%s %s', '>>>>>', patient.name)

            if patient.phase_id.id is not False:

                patient_history = PatientHistory.search([
                    ('patient_id', '=', patient.id),
                    ('phase_id', '=', patient.phase_id.id),
                    ('date_sign_out', '=', False),
                ])

                if patient_history.id is False:

                    patient_history_2 = PatientHistory.search([
                        ('patient_id', '=', patient.id),
                        ('date_sign_out', '=', False),
                    ])
                    if patient_history_2.id is not False:
                        patient_history_2.date_sign_out = self.date_sign_out
                        _logger.info(u'%s %s %s %s', '>>>>>>>>>>', patient_history_2.phase_id.name,
                                                     patient_history_2.date_sign_in,
                                                     patient_history_2.date_sign_out)

                    m2m_list = []
                    for category_id in patient.category_ids:
                        m2m_list.append((4, category_id.id))
                    category_ids = m2m_list
                    m2m_list = []
                    for marker_id in patient.marker_ids:
                        m2m_list.append((4, marker_id.id))
                    marker_ids = m2m_list
                    m2m_list = []
                    for tag_id in patient.tag_ids:
                        m2m_list.append((4, tag_id.id))
                    tag_ids = m2m_list
                    values = {
                        'phase_id': patient.phase_id.id,
                        'date_sign_in': self.date_sign_in,
                        'state': patient.state,
                        'reg_state': patient.reg_state,
                        'employee_id': patient.employee_id.id,
                        'patient_id': patient.id,
                        'category_ids': category_ids,
                        'marker_ids': marker_ids,
                        'tag_ids': tag_ids,
                        'responsible_id': patient.responsible_id.id,
                        'caregiver_id': patient.caregiver_id.id,
                        'family_id': patient.family_id.id,
                        'ref_address_id': patient.ref_address_id.id,
                    }
                    patient_history = PatientHistory.create(values)
                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', patient_history.phase_id.name,
                                                 patient_history.date_sign_in,
                                                 patient_history.date_sign_out)

                else:

                    if patient_history.state != patient.state:
                        patient_history.state = patient.state

                    if patient_history.reg_state != patient.reg_state:
                        patient_history.reg_state = patient.reg_state

                    if patient_history.employee_id.id != patient.employee_id.id:
                        patient_history.employee_id = patient.employee_id.id

                    m2m_list = []
                    for category_id in patient.category_ids:
                        m2m_list.append((4, category_id.id))
                    m2m_list_2 = []
                    for category_id in patient_history.category_ids:
                        m2m_list_2.append((4, category_id.id))
                    if m2m_list != m2m_list_2:
                        patient_history.category_ids = m2m_list

                    m2m_list = []
                    for marker_id in patient.marker_ids:
                        m2m_list.append((4, marker_id.id))
                    m2m_list_2 = []
                    for marker_id in patient_history.marker_ids:
                        m2m_list_2.append((4, marker_id.id))
                    if m2m_list != m2m_list_2:
                        patient_history.marker_ids = m2m_list

                    m2m_list = []
                    for tag_id in patient.tag_ids:
                        m2m_list.append((4, tag_id.id))
                    m2m_list_2 = []
                    for tag_id in patient_history.tag_ids:
                        m2m_list_2.append((4, tag_id.id))
                    if m2m_list != m2m_list_2:
                        patient_history.tag_ids = m2m_list

                    if patient_history.responsible_id.id != patient.responsible_id.id:
                        patient_history.responsible_id = patient.responsible_id.id

                    if patient_history.caregiver_id.id != patient.caregiver_id.id:
                        patient_history.caregiver_id = patient.caregiver_id.id

                    if patient_history.family_id.id != patient.family_id.id:
                        patient_history.family_id = patient.family_id.id

                    if patient_history.ref_address_id.id != patient.ref_address_id.id:
                        patient_history.ref_address_id = patient.ref_address_id.id

                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', patient_history.phase_id.name,
                                                 patient_history.date_sign_in,
                                                 patient_history.date_sign_out)

            else:

                patient_history = PatientHistory.search([
                    ('patient_id', '=', patient.id),
                    ('date_sign_out', '=', False),
                ])

                if patient_history.id is not False:
                    patient_history.date_sign_out = self.date_sign_out
                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', patient_history.phase_id.name,
                                                 patient_history.date_sign_in,
                                                 patient_history.date_sign_out)

        return True
        # return self._reopen_form()
