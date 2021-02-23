# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PersonMassEdit(models.TransientModel):
    _inherit = 'clv.person.mass_edit'

    is_patient = fields.Boolean(
        string='Is Patient'
    )
    is_patient_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Is Patient:', default=False, readonly=False, required=False
    )

    def do_person_mass_edit(self):
        self.ensure_one()

        super().do_person_mass_edit()

        for person in self.person_ids:

            _logger.info(u'%s %s', '>>>>>', person.name)

            if self.is_patient_selection == 'set':
                person.is_patient = self.is_patient
            if self.is_patient_selection == 'remove':
                person.is_patient = False

        return True
