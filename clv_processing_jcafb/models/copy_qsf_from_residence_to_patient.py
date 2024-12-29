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

    def _do_copy_qsf_from_residence_to_patient(self, schedule):

        _logger.info(u'%s %s', '>>>>>>>> schedule:', schedule.name)

        schedule.processing_log = 'Executing: "' + '_do_copy_qsf_from_residence_to_patient' + '"...\n\n'
        schedule.processing_log += '>>>>>>>> schedule:' + schedule.name + '"...\n\n'
        date_last_exec = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        from time import time
        start = time()

        method_args = {}
        if schedule.method_args is not False:
            method_args = literal_eval(schedule.method_args)
        _logger.info(u'%s %s', '>>>>>>>>>> method_args: ', method_args)

        # DocumentMarker = self.env['clv.document.marker']
        Document = self.env['clv.document']
        DocumentType = self.env['clv.document.type']
        DocumentItem = self.env['clv.document.item']
        PatientHistory = self.env['clv.patient.history']

        QSF17_document_type_id = DocumentType.search([('code', '=', 'QSF17')]).id
        QSF18_document_type_id = DocumentType.search([('code', '=', 'QSF18')]).id
        QSF19_document_type_id = DocumentType.search([('code', '=', 'QSF19')]).id
        QSF20_document_type_id = DocumentType.search([('code', '=', 'QSF20')]).id

        QSI17_document_type_id = DocumentType.search([('code', '=', 'QSI17')]).id
        QSI18_document_type_id = DocumentType.search([('code', '=', 'QSI18')]).id
        QSI19_document_type_id = DocumentType.search([('code', '=', 'QSI19')]).id
        QSI20_document_type_id = DocumentType.search([('code', '=', 'QSI20')]).id

        QSC17_document_type_id = DocumentType.search([('code', '=', 'QSC17')]).id
        QSC18_document_type_id = DocumentType.search([('code', '=', 'QSC18')]).id
        QSC19_document_type_id = DocumentType.search([('code', '=', 'QSC19')]).id
        QSC20_document_type_id = DocumentType.search([('code', '=', 'QSC20')]).id

        # has_related_QSF = DocumentMarker.search([
        #     ('name', '=', 'Has related QSF'),
        # ])
        # if has_related_QSF.id is False:
        #     vals = {}
        #     vals['name'] = 'Has related QSF'
        #     has_related_QSF = DocumentMarker.create(vals)

        # has_related_QSI_QSC = DocumentMarker.search([
        #     ('name', '=', 'Has related QSI/QSC'),
        # ])
        # if has_related_QSI_QSC.id is False:
        #     vals = {}
        #     vals['name'] = 'Has related QSI/QSC'
        #     has_related_QSI_QSC = DocumentMarker.create(vals)

        qsf_documents = Document.search([
            ('document_type_id', 'in', [QSF17_document_type_id, QSF18_document_type_id,
                                        QSF19_document_type_id, QSF20_document_type_id]),
        ])

        row_count = 0

        for qsf_document in qsf_documents:

            if qsf_document.ref_id._name == 'clv.residence':

                row_count += 1

                residence = qsf_document.ref_id

                _logger.info(u'%s %s %s (%s) %s', '>>>>>>>>: ',
                             row_count, qsf_document, qsf_document.document_type_id.code, qsf_document.phase_id.name)

                _logger.info(u'%s %s', '>>>>>>>>>>>>>: ',
                             residence.name)

                patient_histories = PatientHistory.search([
                    ('residence_id', '=', residence.id),
                    ('phase_id', '=', qsf_document.phase_id.id),
                ])

                for patient_history in patient_histories:

                    patient = patient_history.patient_id

                    patient_documents = Document.search([
                        ('ref_id', '=', patient._name + ',' + str(patient.id)),
                        ('phase_id', '=', qsf_document.phase_id.id),
                        ('document_type_id', 'in', [QSI17_document_type_id, QSI18_document_type_id,
                                                    QSI19_document_type_id, QSI20_document_type_id,
                                                    QSC17_document_type_id, QSC18_document_type_id,
                                                    QSC19_document_type_id, QSC20_document_type_id]),
                    ])

                    patient_qsf = Document.search([
                        ('ref_id', '=', patient._name + ',' + str(patient.id)),
                        ('phase_id', '=', qsf_document.phase_id.id),
                        ('document_type_id', '=', qsf_document.document_type_id.id),
                    ])

                    _logger.info(u'%s %s', '>>>>>>>>>>>>>>>>>>: ',
                                 patient.name)

                    for patient_document in patient_documents:

                        _logger.info(u'%s %s %s %s', '>>>>>>>>>>>>>>>>>>>>>>>: ',
                                     patient_document.document_type_id.name, patient_document.code,
                                     patient_document.marker_ids.name)

                        if patient_qsf.id is False:

                            qsf_vals = {}
                            # qsf_vals['code'] = '/'
                            qsf_vals['document_type_id'] = qsf_document.document_type_id.id
                            qsf_vals['survey_id'] = qsf_document.survey_id.id
                            qsf_vals['survey_user_input_id'] = qsf_document.survey_user_input_id.id
                            qsf_vals['survey_url'] = qsf_document.survey_url
                            qsf_vals['phase_id'] = qsf_document.phase_id.id
                            qsf_vals['ref_id'] = patient._name + ',' + str(patient.id)

                            # m2m_list = []
                            # for global_tag_id in qsf_document.global_tag_ids:
                            #     m2m_list.append((4, global_tag_id.id))
                            # qsf_vals['global_tag_ids'] = m2m_list

                            m2m_list = []
                            for category_id in qsf_document.category_ids:
                                m2m_list.append((4, category_id.id))
                            qsf_vals['category_ids'] = m2m_list

                            # m2m_list = []
                            # for marker_id in qsf_document.marker_ids:
                            #     m2m_list.append((4, marker_id.id))
                            # qsf_vals['marker_ids'] = m2m_list

                            qsf_vals['reg_state'] = qsf_document.reg_state
                            qsf_vals['state'] = qsf_document.state
                            qsf_vals['items_ok'] = qsf_document.items_ok

                            _logger.info(u'%s %s', '>>>>>>>>>>>>>>>>>>>>>>> vals: ',
                                         qsf_vals)

                            patient_qsf = Document.create(qsf_vals)

                            if patient_qsf.id is not False:

                                _logger.info(u'%s %s', '>>>>>>>>>>>>>>>>>>>>>>>: ',
                                             patient_qsf)

                                if patient_qsf.code is False:
                                    patient_qsf.code = '/'

                                for item_id in qsf_document.item_ids:

                                    item_vals = {}
                                    item_vals['code'] = item_id.code
                                    item_vals['name'] = item_id.name
                                    item_vals['value'] = item_id.value
                                    item_vals['sequence'] = item_id.sequence
                                    item_vals['document_display'] = item_id.document_display
                                    item_vals['document_type_id'] = item_id.document_type_id.id
                                    item_vals['document_type_phase_id'] = item_id.document_type_phase_id.id
                                    item_vals['document_id'] = patient_qsf.id
                                    item_vals['document_phase_id'] = item_id.document_phase_id.id

                                    DocumentItem.create(item_vals)

                                # qsf_document.marker_ids = [(4, has_related_QSI_QSC.id)]
                                # patient_document.marker_ids = [(4, has_related_QSF.id)]
                                patient_qsf.parent_id = qsf_document.id

        _logger.info(u'%s %s', '>>>>>>>> row_count: ', row_count)
        _logger.info(u'%s %s', '>>>>>>>> Execution time: ', secondsToStr(time() - start))

        schedule.processing_log +=  \
            'date_last_exec: ' + str(date_last_exec) + '\n' + \
            'row_count: ' + str(row_count) + '\n' + \
            'Execution time: ' + str(secondsToStr(time() - start)) + '\n'
