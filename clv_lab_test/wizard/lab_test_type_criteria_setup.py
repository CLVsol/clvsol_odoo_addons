# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class LabTestTypeCriterionSetUp(models.TransientModel):
    _description = 'Lab Test Type Criteria Setup'
    _name = 'clv.lab_test.type.criteria_setup'

    def _default_lab_test_type_ids(self):
        return self._context.get('active_ids')
    lab_test_type_ids = fields.Many2many(
        comodel_name='clv.lab_test.type',
        relation='clv_lab_test_type_criteria_setup_rel',
        string='Lab Test Types',
        default=_default_lab_test_type_ids
    )

    def _reopen_form(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
        return action

    def do_lab_test_type_criteria_setup(self):
        self.ensure_one()

        return True
