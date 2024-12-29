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

    def _do_patient_estilmated_age_updt(self, schedule):

        _logger.info(u'%s %s', '>>>>>>>> schedule:', schedule.name)

        schedule.processing_log = 'Executing: "' + '_do_patient_estilmated_age_updt' + '"...\n\n'
        schedule.processing_log += '>>>>>>>> schedule:' + schedule.name + '"...\n\n'
        date_last_exec = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        from time import time
        start = time()

        method_args = {}
        if schedule.method_args is not False:
            method_args = literal_eval(schedule.method_args)
        _logger.info(u'%s %s', '>>>>>>>>>> method_args: ', method_args)

        Patient = self.env['clv.patient']

        patients = Patient.search([])

        row_count = 0

        for patient in patients:

            row_count += 1

            _logger.info(u'%s %s %s (%s)', '>>>>>>>> Patient: ', row_count, patient.name, patient.estimated_age)

            if patient.estimated_age is not False:

                increment = method_args['increment']
                patient.estimated_age = str(int(patient.estimated_age) + increment)

                _logger.info(u'%s %s (%s)', '>>>>>>>>>>>> Patient: ', patient.name, patient.estimated_age)

        _logger.info(u'%s %s', '>>>>>>>>>>>>> row_count: ', row_count)
        _logger.info(u'%s %s', '>>>>>>>> Execution time: ', secondsToStr(time() - start))

        schedule.processing_log +=  \
            'date_last_exec: ' + str(date_last_exec) + '\n' + \
            'row_count: ' + str(row_count) + '\n' + \
            'Execution time: ' + str(secondsToStr(time() - start)) + '\n'
