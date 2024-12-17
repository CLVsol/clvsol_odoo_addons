# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class EventAttendeePatientMassEdit(models.TransientModel):
    _description = 'Event Attendee Patient Mass Edit'
    _name = 'clv.event.attendee.patient_mass_edit'

    def _default_event_attendee_ids(self):
        return self._context.get('active_ids')
    event_attendee_ids = fields.Many2many(
        comodel_name='clv.event.attendee',
        relation='clv_event_attendee_patient_mass_edit_rel',
        string='Event Attendees',
        default=_default_event_attendee_ids
    )

    marker_ids = fields.Many2many(
        comodel_name='clv.patient.marker',
        relation='clv_event_attendee_patient_mass_edit_marker_rel',
        column1='event_attendee_id',
        column2='patient_marker_id',
        string='Patient Markers'
    )
    marker_ids_selection = fields.Selection(
        [('add', 'Add'),
         ('remove_m2m', 'Remove'),
         ('set', 'Set'),
         ], string='Patient Markers:', default=False, readonly=False, required=False
    )

    def do_event_attendee_patient_mass_edit(self):
        self.ensure_one()

        for event_attendee in self.event_attendee_ids:

            _logger.info(u'%s %s', '>>>>>', event_attendee)

            PatientModel = self.env[event_attendee.ref_model]
            if PatientModel._name != 'clv.patient':
                return True

            patient = PatientModel.with_context({'active_test': False}).search([
                ('id', '=', event_attendee.ref_id.id),
            ])

            _logger.info(u'%s %s', '>>>>>>>>>>', patient.name)

            if self.marker_ids_selection == 'add':
                m2m_list = []
                for patient_marker_id in self.marker_ids:
                    m2m_list.append((4, patient_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.marker_ids = m2m_list
            if self.marker_ids_selection == 'remove_m2m':
                m2m_list = []
                for patient_marker_id in self.marker_ids:
                    m2m_list.append((3, patient_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.marker_ids = m2m_list
            if self.marker_ids_selection == 'set':
                m2m_list = []
                for patient_marker_id in patient.marker_ids:
                    m2m_list.append((3, patient_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.marker_ids = m2m_list
                m2m_list = []
                for patient_marker_id in self.marker_ids:
                    m2m_list.append((4, patient_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.marker_ids = m2m_list

        return True
