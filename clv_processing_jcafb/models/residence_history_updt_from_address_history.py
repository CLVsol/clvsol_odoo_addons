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

    def _do_residence_history_updt_from_address_history(self, schedule):

        _logger.info(u'%s %s', '>>>>>>>> schedule:', schedule.name)

        schedule.processing_log = 'Executing: "' + '_do_residence_history_updt_from_address_history' + '"...\n\n'
        schedule.processing_log += '>>>>>>>> schedule:' + schedule.name + '"...\n\n'
        date_last_exec = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        from time import time
        start = time()

        method_args = {}
        if schedule.method_args is not False:
            method_args = literal_eval(schedule.method_args)
        _logger.info(u'%s %s', '>>>>>>>>>> method_args: ', method_args)

        AddressHistory = self.env['clv.address.history']
        Residence = self.env['clv.residence']
        Residence = self.env['clv.residence']
        ResidenceHistory = self.env['clv.residence.history']
        ResidenceCategory = self.env['clv.residence.category']
        ResidenceMarker = self.env['clv.residence.marker']
        ResidenceTag = self.env['clv.residence.tag']

        address_histories = AddressHistory.search([])

        row_count = 0

        for address_history in address_histories:

            row_count += 1

            _logger.info(u'%s %s %s', '>>>>>>>> Address History: ', row_count, address_history)

            if address_history.is_residence_history is False:

                vals = {}

                residence = Residence.search([
                    ('code', '=', address_history.address_id.code),
                ])

                if residence.id is not False:

                    vals['residence_id'] = residence.id

                    vals['phase_id'] = address_history.phase_id.id
                    vals['date_sign_in'] = address_history.date_sign_in
                    vals['date_sign_out'] = address_history.date_sign_out
                    vals['employee_id'] = address_history.employee_id.id
                    vals['reg_state'] = address_history.reg_state
                    vals['state'] = address_history.state

                    m2m_list = []
                    for category_id in address_history.category_ids:
                        residence_category = ResidenceCategory.search([
                            ('name', '=', category_id.name),
                        ])
                        m2m_list.append((4, residence_category.id))
                    if m2m_list != []:
                        vals['category_ids'] = m2m_list

                    m2m_list = []
                    for marker_id in address_history.marker_ids:
                        residence_marker = ResidenceMarker.search([
                            ('name', '=', marker_id.name),
                        ])
                        m2m_list.append((4, residence_marker.id))
                    if m2m_list != []:
                        vals['marker_ids'] = m2m_list

                    m2m_list = []
                    for tag_id in address_history.tag_ids:
                        residence_tag = ResidenceTag.search([
                            ('name', '=', tag_id.name),
                        ])
                        m2m_list.append((4, residence_tag.id))
                    if m2m_list != []:
                        vals['tag_ids'] = m2m_list

                    vals['related_address_history_is_unavailable'] = False
                    vals['related_address_history_id'] = address_history.id

                    residence_history = ResidenceHistory.create(vals)

                    address_history.is_residence_history = True

                    _logger.info(u'%s %s %s', '>>>>>>>>>>>> Residence History: ', row_count, residence_history)

        _logger.info(u'%s %s', '>>>>>>>>>>>>> row_count: ', row_count)
        _logger.info(u'%s %s', '>>>>>>>> Execution time: ', secondsToStr(time() - start))

        schedule.processing_log +=  \
            'date_last_exec: ' + str(date_last_exec) + '\n' + \
            'row_count: ' + str(row_count) + '\n' + \
            'Execution time: ' + str(secondsToStr(time() - start)) + '\n'
