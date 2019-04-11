# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import models, fields

_logger = logging.getLogger(__name__)


def secondsToStr(t):

    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class AbstractVerification(models.AbstractModel):
    _description = 'Abstract Verification'
    _name = 'clv.abstract.verification'

    date_verification = fields.Datetime(string="Verification Date")
    verification_status = fields.Selection(
        [('unknown', 'Unknown'),
         ('failed', 'Failed'),
         ('ok', 'Ok'),
         ('missing', 'Missing'),
         ], string='Verification Status', default='unknown'
    )
    verification_outcomes = fields.Text(string='Verification Outcomes')

    def _object_verification(self, schedule, model_name):

        from time import time
        start = time()

        _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

        schedule.verification_log +=  \
            'Execution time: ' + str(secondsToStr(time() - start)) + '\n'
