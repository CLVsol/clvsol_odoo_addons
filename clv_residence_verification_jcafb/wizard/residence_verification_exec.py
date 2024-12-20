# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class ResidenceVerificationExecute(models.TransientModel):
    _description = 'Residence Verification Execute'
    _name = 'clv.residence.verification_exec'

    def _default_residence_ids(self):
        return self._context.get('active_ids')
    residence_ids = fields.Many2many(
        comodel_name='clv.residence',
        relation='clv_residence_verification_outcome_refresh_rel',
        string='Residences',
        default=_default_residence_ids)
    count_residences = fields.Integer(
        string='Number of Residences',
        compute='_compute_count_residences',
        store=False
    )

    @api.depends('residence_ids')
    def _compute_count_residences(self):
        for r in self:
            r.count_residences = len(r.residence_ids)

    def do_residence_verification_exec(self):
        self.ensure_one()

        for residence in self.residence_ids:

            residence._residence_verification_exec()

        return True
