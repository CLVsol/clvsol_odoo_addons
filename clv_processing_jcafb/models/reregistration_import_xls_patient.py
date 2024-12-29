# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from functools import reduce
from ast import literal_eval
import xlrd
from datetime import datetime

from odoo import models

_logger = logging.getLogger(__name__)


def secondsToStr(t):

    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class AbstractProcess(models.AbstractModel):
    _inherit = 'clv.abstract.process'

    def _do_reregistration_import_xls_patient(self, schedule):

        _logger.info(u'%s %s', '>>>>>>>> schedule:', schedule.name)

        schedule.processing_log = 'Executing: "' + '_do_reregistration_import_xls_patient' + '"...\n\n'
        schedule.processing_log += '>>>>>>>> schedule:' + schedule.name + '"...\n\n'
        date_last_exec = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        from time import time
        start = time()

        method_args = {}
        if schedule.method_args is not False:
            method_args = literal_eval(schedule.method_args)
        _logger.info(u'%s %s', '>>>>>>>>>> method_args: ', method_args)

        filepath = method_args['file_path']
        _logger.info(u'>>>>>>>>>> file_path: %s', filepath)
        sheet_name = method_args['sheet_name']
        _logger.info(u'>>>>>>>>>> sheet_name: %s', sheet_name)

        book = xlrd.open_workbook(filepath)
        sheet = book.sheet_by_name(sheet_name)

        Patient = self.env['clv.patient']
        PatientAux = self.env['clv.patient_aux']

        param_value = self.env['ir.config_parameter'].sudo().get_param(
            'clv.global_settings.current_phase_id', '').strip()
        phase_id = False
        if param_value:
            phase_id = int(param_value)

        CEP = '17455-000'

        row_count = 0
        reg_count_x = 0
        reg_count_0 = 0
        reg_count_1 = 0
        reg_count_2 = 0
        reg_count_3 = 0
        reg_count_4 = 0
        reg_count_5 = 0

        for i in range(sheet.nrows):

            row_count += 1

            rec = sheet.cell_value(i, 0)
            ok = sheet.cell_value(i, 1)
            # patient = sheet.cell_value(i, 2)
            # projeto = sheet.cell_value(i, 3)
            # patient_code = sheet.cell_value(i, 4)
            patient_name = sheet.cell_value(i, 5)
            gender = sheet.cell_value(i, 6)
            date_of_birth = sheet.cell_value(i, 7)
            address_name = sheet.cell_value(i, 8)
            # district = sheet.cell_value(i, 9)
            # city = sheet.cell_value(i, 10)
            # responsible = shOk: %seet.cell_value(i, 11)

            if ok == 'x':

                reg_count_x += 1

                _logger.info(u'>>>>>>>>>> Rec: %s, Ok: %s, Name: %s, Address: %s', rec, ok, patient_name, address_name)

                patient = Patient.search([
                    ('name', '=', patient_name),
                ])
                _logger.info(u'>>>>>>>>>>>>>>>> Patient: %s', patient)

                patient_aux = PatientAux.search([
                    ('name', '=', patient_name),
                ])
                _logger.info(u'>>>>>>>>>>>>>>>> Patient (Aux): %s', patient_aux)

                if patient_aux.id is not False:

                    new_patient = False

                    _logger.info(u'>>>>>>>>>>>>>>>>>>>>> Related Patient: %s', patient_aux.related_patient_id)

                else:

                    new_patient = True

                new_address = False

                if address_name == patient_aux.address_name:

                    change_address = False

                else:

                    change_address = True

                    if address_name is False or address_name == '':
                        new_address = 'NULL'

                _logger.info(u'>>>>>>>>>>>>>>>> New Patient: %s', new_patient)
                _logger.info(u'>>>>>>>>>>>>>>>> Change Address: %s', change_address)
                _logger.info(u'>>>>>>>>>>>>>>>> New Address: %s', new_address)

                if new_patient is False and change_address is False and new_address != 'NULL':

                    reg_count_0 += 1
                    _logger.info(u'>>>>>>>>>>>>>>>> [0]: %s', reg_count_0)

                    if patient_aux.reg_state != 'revised':
                        patient_aux.reg_state = 'revised'
                    if patient_aux.state != 'available':
                        patient_aux.state = 'available'
                    if patient_aux.phase_id.id != phase_id:
                        patient_aux.phase_id = phase_id

                elif new_patient is False and change_address is True and new_address != 'NULL':

                    reg_count_1 += 1
                    _logger.info(u'>>>>>>>>>>>>>>>> [1]: %s', reg_count_1)

                    vals = {}
                    patient_aux.zip = CEP
                    patient_aux.zip_search()
                    street_name = address_name[:address_name.find(',')]
                    street_number = address_name[address_name.find(', ') + 2:address_name.find('(') - 1]
                    street_number2 = False
                    street2 = address_name[address_name.find('(') + 1:address_name.find(')')]
                    patient_aux.street_name = street_name
                    patient_aux.street2 = street2
                    patient_aux.street_number = street_number
                    patient_aux.street_number2 = street_number2

                    if patient_aux.reg_state != 'revised':
                        patient_aux.reg_state = 'revised'
                    if patient_aux.state != 'available':
                        patient_aux.state = 'available'
                    if patient_aux.phase_id.id != phase_id:
                        patient_aux.phase_id = phase_id

                elif new_patient is False and change_address is True and new_address == 'NULL':

                    reg_count_5 += 1
                    _logger.info(u'>>>>>>>>>>>>>>>> [5]: %s', reg_count_5)

                    patient_aux.do_patient_aux_clear_address_data()
                    patient_aux.contact_info_is_unavailable = True

                    if patient_aux.reg_state != 'revised':
                        patient_aux.reg_state = 'revised'
                    if patient_aux.state != 'unavailable':
                        patient_aux.state = 'unavailable'
                    if patient_aux.phase_id.id != phase_id:
                        patient_aux.phase_id = phase_id

                elif new_patient is True and change_address is True and new_address != 'NULL':

                    reg_count_3 += 1
                    _logger.info(u'>>>>>>>>>>>>>>>> [3]: %s', reg_count_3)

                    vals = {}
                    vals['name'] = patient_name
                    vals['gender'] = gender[:1]
                    datetime_date = xlrd.xldate_as_datetime(date_of_birth, 0)
                    date_object = datetime_date.date()
                    string_date = date_object.isoformat()
                    vals['birthday'] = datetime.strptime(string_date, '%Y-%m-%d')

                    patient_aux = PatientAux.create(vals)

                    patient_aux.zip = CEP
                    patient_aux.zip_search()
                    street_name = address_name[:address_name.find(',')]
                    street_number = address_name[address_name.find(', ') + 2:address_name.find('(') - 1]
                    street_number2 = False
                    street2 = address_name[address_name.find('(') + 1:address_name.find(')')]
                    patient_aux.street_name = street_name
                    patient_aux.street2 = street2
                    patient_aux.street_number = street_number
                    patient_aux.street_number2 = street_number2

                    if patient_aux.reg_state != 'revised':
                        patient_aux.reg_state = 'revised'
                    if patient_aux.state != 'available':
                        patient_aux.state = 'available'
                    if patient_aux.phase_id.id != phase_id:
                        patient_aux.phase_id = phase_id

        _logger.info(u'%s %s', '>>>>>>>>>>>>> row_count: ', row_count)
        _logger.info(u'%s %s', '>>>>>>>>>>>>> reg_count_x: ', reg_count_x)
        _logger.info(u'%s %s', '>>>>>>>>>>>>> reg_count_0: ', reg_count_0)
        _logger.info(u'%s %s', '>>>>>>>>>>>>> reg_count_1: ', reg_count_1)
        _logger.info(u'%s %s', '>>>>>>>>>>>>> reg_count_2: ', reg_count_2)
        _logger.info(u'%s %s', '>>>>>>>>>>>>> reg_count_3: ', reg_count_3)
        _logger.info(u'%s %s', '>>>>>>>>>>>>> reg_count_4: ', reg_count_4)
        _logger.info(u'%s %s', '>>>>>>>>>>>>> reg_count_5: ', reg_count_5)
        _logger.info(u'%s %s', '>>>>>>>> Execution time: ', secondsToStr(time() - start))

        schedule.processing_log +=  \
            'date_last_exec: ' + str(date_last_exec) + '\n' + \
            'row_count: ' + str(row_count) + '\n' + \
            'reg_count_x: ' + str(reg_count_x) + '\n' + \
            'reg_count_0: ' + str(reg_count_0) + '\n' + \
            'reg_count_1: ' + str(reg_count_1) + '\n' + \
            'reg_count_2: ' + str(reg_count_2) + '\n' + \
            'reg_count_3: ' + str(reg_count_3) + '\n' + \
            'reg_count_4: ' + str(reg_count_4) + '\n' + \
            'reg_count_5: ' + str(reg_count_5) + '\n' + \
            'Execution time: ' + str(secondsToStr(time() - start)) + '\n'
