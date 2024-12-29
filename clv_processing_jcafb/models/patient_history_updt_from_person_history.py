# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from functools import reduce
from ast import literal_eval
from datetime import datetime

from odoo import models

_logger = logging.getLogger(__name__)


def secondsToStr(t):

    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class AbstractProcess(models.AbstractModel):
    _inherit = 'clv.abstract.process'

    def _do_patient_history_updt_from_person_history(self, schedule):

        _logger.info(u'%s %s', '>>>>>>>> schedule:', schedule.name)

        schedule.processing_log = 'Executing: "' + '_do_patient_history_updt_from_person_history' + '"...\n\n'
        schedule.processing_log += '>>>>>>>> schedule:' + schedule.name + '"...\n\n'
        date_last_exec = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        from time import time
        start = time()

        method_args = {}
        if schedule.method_args is not False:
            method_args = literal_eval(schedule.method_args)
        _logger.info(u'%s %s', '>>>>>>>>>> method_args: ', method_args)

        PersonHistory = self.env['clv.person.history']
        Patient = self.env['clv.patient']
        Residence = self.env['clv.residence']
        PatientHistory = self.env['clv.patient.history']
        PatientCategory = self.env['clv.patient.category']
        PatientMarker = self.env['clv.patient.marker']
        PatientTag = self.env['clv.patient.tag']
        AddressHistory = self.env['clv.address.history']

        person_histories = PersonHistory.search([])

        row_count = 0

        for person_history in person_histories:

            row_count += 1

            _logger.info(u'%s %s %s', '>>>>>>>> Person History: ', row_count, person_history)

            if person_history.is_patient_history is False:

                vals = {}

                patient = Patient.search([
                    ('code', '=', person_history.person_id.code),
                ])
                if patient.id is not False:

                    vals['patient_id'] = patient.id

                    vals['address_name'] = person_history.ref_address_id.name
                    vals['phase_id'] = person_history.phase_id.id
                    vals['date_sign_in'] = person_history.date_sign_in
                    vals['date_sign_out'] = person_history.date_sign_out
                    vals['reg_state'] = person_history.reg_state
                    vals['state'] = person_history.state

                    address_history = AddressHistory.search([
                        ('phase_id', '=', person_history.phase_id.id),
                        ('address_id', '=', person_history.ref_address_id.id),
                    ])
                    vals['employee_id'] = address_history.employee_id.id

                    m2m_list = []
                    for category_id in person_history.category_ids:
                        patient_category = PatientCategory.search([
                            ('name', '=', category_id.name),
                        ])
                        m2m_list.append((4, patient_category.id))
                    if m2m_list != []:
                        vals['category_ids'] = m2m_list

                    m2m_list = []
                    for marker_id in person_history.marker_ids:
                        patient_marker = PatientMarker.search([
                            ('name', '=', marker_id.name),
                        ])
                        m2m_list.append((4, patient_marker.id))
                    if m2m_list != []:
                        vals['marker_ids'] = m2m_list

                    m2m_list = []
                    for tag_id in person_history.tag_ids:
                        patient_tag = PatientTag.search([
                            ('name', '=', tag_id.name),
                        ])
                        m2m_list.append((4, patient_tag.id))
                    if m2m_list != []:
                        vals['tag_ids'] = m2m_list

                    residence = Residence.search([
                        ('code', '=', person_history.ref_address_id.code),
                    ])
                    if residence.id is not False:
                        vals['residence_id'] = residence.id

                    vals['related_person_history_is_unavailable'] = False
                    vals['related_person_history_id'] = person_history.id

                    patient_history = PatientHistory.create(vals)

                    person_history.is_patient_history = True

                    _logger.info(u'%s %s %s', '>>>>>>>>>>>> Patient History: ', row_count, patient_history)

        _logger.info(u'%s %s', '>>>>>>>>>>>>> row_count: ', row_count)
        _logger.info(u'%s %s', '>>>>>>>> Execution time: ', secondsToStr(time() - start))

        schedule.processing_log +=  \
            'date_last_exec: ' + str(date_last_exec) + '\n' + \
            'row_count: ' + str(row_count) + '\n' + \
            'Execution time: ' + str(secondsToStr(time() - start)) + '\n'
