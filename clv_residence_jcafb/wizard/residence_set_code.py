# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResidenceSetCode(models.TransientModel):
    _description = 'Residence Set Code'
    _name = 'clv.residence.set_code'

    def _default_patientaux_ids(self):
        return self._context.get('active_ids')
    residence_ids = fields.Many2many(
        comodel_name='clv.residence',
        relation='clv_residence_set_code_rel',
        string='Residences',
        default=_default_patientaux_ids
    )

    residence_verification_exec = fields.Boolean(
        string='Residence Verification Execute',
        default=True,
    )

    def do_residence_set_code(self):
        self.ensure_one()

        for residence in self.residence_ids:

            _logger.info(u'%s %s', '>>>>>', residence.name)

            residence._residence_set_code()

            if self.residence_verification_exec:
                residence._residence_verification_exec()

        return True
