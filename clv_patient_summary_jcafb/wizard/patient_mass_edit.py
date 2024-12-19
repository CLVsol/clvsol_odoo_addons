# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatientMassEdit(models.TransientModel):
    _inherit = 'clv.patient.mass_edit'

    summary_id = fields.Many2one(
        comodel_name='clv.summary',
        string='Summary'
    )
    summary_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Summary:', default=False, readonly=False, required=False
    )

    def do_patient_mass_edit(self):
        self.ensure_one()

        super().do_patient_mass_edit()

        for patient in self.patient_ids:

            _logger.info(u'%s %s', '>>>>>', patient.name)

            if self.summary_id_selection == 'set':
                patient.summary_id = self.summary_id
            if self.summary_id_selection == 'remove':
                patient.summary_id = False

        return True
