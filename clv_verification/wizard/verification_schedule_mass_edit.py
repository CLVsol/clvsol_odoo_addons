# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class VerificationScheduleMassEdit(models.TransientModel):
    _description = 'Verification Schedule Mass Edit'
    _name = 'clv.verification.schedule.mass_edit'

    def _default_verification_schedule_ids(self):
        return self._context.get('active_ids')
    verification_schedule_ids = fields.Many2many(
        comodel_name='clv.verification.schedule',
        relation='clv_verification_schedule_mass_edit_rel',
        string='Verification Schedules',
        default=_default_verification_schedule_ids
    )

    def do_verification_schedule_mass_edit(self):
        self.ensure_one()

        for verification_schedule in self.verification_schedule_ids:

            _logger.info(u'%s %s', '>>>>>', verification_schedule.name)

        return True
