# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce
from datetime import datetime

from odoo import models, fields

_logger = logging.getLogger(__name__)


def secondsToStr(t):

    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class AbstractVerification(models.AbstractModel):
    _description = 'Abstract Verification'
    _name = 'clv.abstract.verification'

    date_verification = fields.Datetime(string="Verification Date")
    state = fields.Selection(
        [('unknown', 'Unknown'),
         ('updated', 'Updated'),
         ('warned', 'Warned'),
         ('failed', 'Failed'),
         ('ok', 'Ok'),
         ('missing', 'Missing'),
         ], string='State', default='unknown'
    )
    verification_outcomes = fields.Text(string='Verification Outcomes')

    def _object_verify(self, schedule):

        model_name = schedule.model

        ModelObject = self.env[model_name]
        model_object = ModelObject.with_context({'active_test': False}).search([
            ('id', '=', self.res_id),
        ])

        _logger.info(u'%s %s', '>>>>>>>>>> (model_object):', model_object)

        _logger.info(u'%s %s', '>>>>>>>>>> (verification):', self)

        self.state = 'ok'

    def _object_verification(self, schedule):

        if (not schedule.verification_disable_identification) or (not schedule.verification_disable_check_missing):
            self._object_verification_identify(schedule)

        from time import time
        start = time()

        if (not schedule.verification_disable_inclusion) or \
           (not schedule.verification_disable_verification):

            Verification = self.env['clv.verification']

            model_name = schedule.model

            verification_max_task = schedule.verification_max_task

            date_last_sync = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            upmost_last_update = False

            schedule.verification_log += 'Executing: "' + '_object_verification' + '"...\n\n'

            verification_objects = Verification.with_context({'active_test': False}).search([
                ('model', '=', model_name),
                ('state', '!=', 'missing'),
                ('state', '!=', 'ok'),
            ])
            _logger.info(u'%s %s', '>>>>>>>>>> (verification_objects):', len(verification_objects))

            reg_count = 0
            include_count = 0
            update_count = 0
            verification_count = 0
            verification_include_count = 0
            verification_update_count = 0
            task_count = 0
            for verification_object in verification_objects:

                reg_count += 1

                _logger.info(u'%s %s %s %s', '>>>>>>>>>>', reg_count,
                             verification_object.res_id,
                             verification_object.res_last_update, )

                if task_count >= verification_max_task:
                    continue

                if upmost_last_update is False:
                    upmost_last_update = verification_object.res_last_update
                else:
                    if verification_object.res_last_update is not False:
                        if verification_object.res_last_update > upmost_last_update:
                            upmost_last_update = verification_object.res_last_update

                if verification_object.res_id == 0:

                    include_count += 1
                    task_count += 1

                    verification_object._object_verify(schedule)

                    self.env.cr.commit()

                else:

                    if verification_object.date_verification is False or \
                       ((verification_object.date_verification >
                         verification_object.res_last_update) and
                            verification_object.state != 'unknown'):

                        update_count += 1
                        task_count += 1

                        verification_object.state = 'updated'

                    if (verification_object.state == 'unknown' or
                        verification_object.state == 'updated') and \
                       schedule.verification_disable_verification is False:

                        verification_count += 1
                        task_count += 1

                        _logger.info(u'>>>>>>>>>>>>>>> %s %s', verification_count, verification_object)

                        if verification_object.state == 'unknown':
                            verification_include_count += 1

                        if verification_object.state == 'updated':
                            verification_update_count += 1

                        verification_object._object_verify(schedule)

                    self.env.cr.commit()

            _logger.info(u'%s %s', '>>>>>>>>>> verification_max_task: ', verification_max_task)
            _logger.info(u'%s %s', '>>>>>>>>>> verification_objects: ', len(verification_objects))
            _logger.info(u'%s %s', '>>>>>>>>>> reg_count: ', reg_count)
            _logger.info(u'%s %s', '>>>>>>>>>> include_count: ', include_count)
            _logger.info(u'%s %s', '>>>>>>>>>> update_count: ', update_count)
            _logger.info(u'%s %s', '>>>>>>>>>> verification_include_count: ', verification_include_count)
            _logger.info(u'%s %s', '>>>>>>>>>> verification_update_count: ', verification_update_count)
            _logger.info(u'%s %s', '>>>>>>>>>> verification_count: ', verification_count)
            _logger.info(u'%s %s', '>>>>>>>>>> task_count: ', task_count)
            _logger.info(u'%s %s', '>>>>>>>>>> date_last_sync: ', date_last_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> upmost_last_update: ', upmost_last_update)
            _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

            schedule.date_last_sync = date_last_sync
            schedule.upmost_last_update = upmost_last_update
            schedule.verification_log +=  \
                'verification_objects: ' + str(len(verification_objects)) + '\n' + \
                'reg_count: ' + str(reg_count) + '\n' + \
                'include_count: ' + str(include_count) + '\n' + \
                'update_count: ' + str(update_count) + '\n' + \
                'verification_include_count: ' + str(verification_include_count) + '\n' + \
                'verification_update_count: ' + str(verification_update_count) + '\n' + \
                'verification_count: ' + str(verification_count) + '\n\n' + \
                'task_count: ' + str(task_count) + '\n\n' + \
                'date_last_sync: ' + str(date_last_sync) + '\n' + \
                'upmost_last_update: ' + str(upmost_last_update) + '\n\n' + \
                'Execution time: ' + str(secondsToStr(time() - start)) + '\n'

    def _object_verification_identify(self, schedule):

        from time import time
        start = time()

        model_name = schedule.model

        ModelObject = self.env[model_name]
        Verification = self.env['clv.verification']

        verification_disable_identification = schedule.verification_disable_identification
        verification_disable_check_missing = schedule.verification_disable_check_missing

        verification_max_task = schedule.verification_max_task
        upmost_last_update = False
        date_last_sync = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        schedule.verification_log += 'Executing: "' + '_object_verification_identify' + '"...\n\n'

        verification_object_ids = []
        verifications = []
        missing_count = 0
        reg_count_2 = 0
        if not verification_disable_check_missing:

            verification_object_ids = []
            model_objects = ModelObject.with_context({'active_test': False}).search([])
            for model_object in model_objects:
                verification_object_ids.append(model_object.id)
            _logger.info(u'%s %s', '>>>>>>>>>> (verification_objects):', len(verification_object_ids))

            verifications = Verification.with_context({'active_test': False}).search([
                ('model', '=', model_name),
                ('res_id', '!=', False),
                ('state', '!=', 'missing'),
            ])
            _logger.info(u'%s %s', '>>>>>>>>>> (verifications):', len(verifications))

            for verification in verifications:
                _logger.info(u'%s %s %s', '>>>>>>>>>>', reg_count_2, verification, )
                if verification.res_id not in verification_object_ids:
                    missing_count += 1
                    _logger.info(u'%s %s %s', '>>>>>>>>>>>>>>> (missing_object):', missing_count, verification.id)
                    verification.verification_outcomes = \
                        verification.model + ' (' + str(verification.res_id) + ') - ' + verification.reference_name
                    verification.res_id = 0
                    verification.state = 'missing'
                reg_count_2 += 1
                self.env.cr.commit()

        verification_args = schedule.verification_last_update_args()
        verification_objects = []
        reg_count = 0
        include_count = 0
        update_count = 0
        task_count = 0
        if not verification_disable_identification:

            verification_args = schedule.verification_last_update_args()
            _logger.info(u'%s %s', '>>>>>>>>>> (verification_args):', verification_args)

            verification_objects = ModelObject.with_context({'active_test': False}).search(
                verification_args
            )

            _logger.info(u'%s %s', '>>>>>>>>>> (verification_objects):', len(verification_objects))

            for verification_object in verification_objects:

                reg_count += 1

                _logger.info(u'%s %s %s %s', '>>>>>>>>>>', reg_count,
                             verification_object['id'],
                             verification_object['__last_update'], )

                if task_count >= verification_max_task:
                    continue

                if upmost_last_update is False:
                    upmost_last_update = verification_object['__last_update']
                else:
                    if verification_object['__last_update'] > upmost_last_update:
                        upmost_last_update = verification_object['__last_update']

                verification = Verification.with_context({'active_test': False}).search([
                    ('model', '=', model_name),
                    ('res_id', '=', verification_object['id']),
                ])

                if verification.id is False:

                    task_count += 1

                    include_count += 1

                    verification_values = {}
                    verification_values['model'] = model_name
                    verification_values['res_id'] = verification_object['id']
                    verification_values['res_last_update'] = verification_object['__last_update']
                    verification_values['state'] = 'unknown'
                    _logger.info(u'>>>>>>>>>>>>>>> %s %s', include_count, verification_values)
                    Verification.create(verification_values)

                    self.env.cr.commit()

                else:

                    if verification.res_last_update is not False:
                        if verification_object['__last_update'] > verification.res_last_update:

                            task_count += 1
                            update_count += 1

                            verification.res_last_update = verification_object['__last_update']

                            if verification.state == 'ok':
                                verification.state = 'updated'

                            _logger.info(u'>>>>>>>>>>>>>>> %s %s', update_count, verification)

                            self.env.cr.commit()

        _logger.info(u'%s %s', '>>>>>>>>>> verification_max_task: ', verification_max_task)
        _logger.info(u'%s %s', '>>>>>>>>>> verification_args: ', verification_args)
        _logger.info(u'%s %s', '>>>>>>>>>> verification_object_ids: ', len(verification_object_ids))
        _logger.info(u'%s %s', '>>>>>>>>>> verifications: ', len(verifications))
        _logger.info(u'%s %s', '>>>>>>>>>> reg_count_2: ', reg_count_2)
        _logger.info(u'%s %s', '>>>>>>>>>> missing_count: ', missing_count)
        _logger.info(u'%s %s', '>>>>>>>>>> reg_count: ', reg_count)
        _logger.info(u'%s %s', '>>>>>>>>>> include_count: ', include_count)
        _logger.info(u'%s %s', '>>>>>>>>>> update_count: ', update_count)
        _logger.info(u'%s %s', '>>>>>>>>>> task_count: ', task_count)
        _logger.info(u'%s %s', '>>>>>>>>>> date_last_sync: ', date_last_sync)
        _logger.info(u'%s %s', '>>>>>>>>>> upmost_last_update: ', upmost_last_update)
        _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

        schedule.date_last_sync = date_last_sync
        schedule.upmost_last_update = upmost_last_update
        schedule.verification_log +=  \
            'verification_args: ' + str(verification_args) + '\n\n' + \
            'verification_object_ids: ' + str(len(verification_object_ids)) + '\n' + \
            'verifications: ' + str(len(verifications)) + '\n' + \
            'reg_count_2: ' + str(reg_count_2) + '\n' + \
            'missing_count: ' + str(missing_count) + '\n\n' + \
            'verification_objects: ' + str(len(verification_objects)) + '\n' + \
            'reg_count: ' + str(reg_count) + '\n' + \
            'include_count: ' + str(include_count) + '\n' + \
            'update_count: ' + str(update_count) + '\n' + \
            'task_count: ' + str(task_count) + '\n\n' + \
            'date_last_sync: ' + str(date_last_sync) + '\n' + \
            'upmost_last_update: ' + str(upmost_last_update) + '\n\n' + \
            'Execution time: ' + str(secondsToStr(time() - start)) + '\n\n'
