# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class VerificationTemplateMassEdit(models.TransientModel):
    _description = 'Verification Template Mas Edit'
    _name = 'clv.verification.template.mass_edit'

    def _default_verification_template_ids(self):
        return self._context.get('active_ids')
    verification_template_ids = fields.Many2many(
        comodel_name='clv.verification.template',
        relation='clv_verification_template_mass_edit_rel',
        string='Verification Templates',
        default=_default_verification_template_ids
    )

    def do_verification_template_mass_edit(self):
        self.ensure_one()

        for verification_template in self.verification_template_ids:

            _logger.info(u'%s %s', '>>>>>', verification_template.name)

        return True
