# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class LabTestTypeExportXlsParamVerificationExecute(models.TransientModel):
    _description = 'Lab Test Type Export XLS Param Verification Execute'
    _name = 'clv.lab_test.export_xls.param.verification_exec'

    def _default_lab_test_export_xls_param_ids(self):
        return self._context.get('active_ids')
    lab_test_export_xls_param_ids = fields.Many2many(
        comodel_name='clv.lab_test.export_xls.param',
        relation='lab_test_export_xls_param_verification_outcome_refresh_rel',
        string='Lab Test Type Export XLS Param',
        default=_default_lab_test_export_xls_param_ids)
    count_lab_test_export_xls_params = fields.Integer(
        string='Number of Lab Test Type Export XLS Param',
        compute='_compute_count_lab_test_export_xls_params',
        store=False
    )

    @api.depends('lab_test_export_xls_param_ids')
    def _compute_count_lab_test_export_xls_params(self):
        for r in self:
            r.count_lab_test_export_xls_params = len(r.lab_test_export_xls_param_ids)

    def do_lab_test_export_xls_param_verification_exec(self):
        self.ensure_one()

        for lab_test_export_xls_param in self.lab_test_export_xls_param_ids:

            lab_test_export_xls_param._lab_test_export_xls_param_verification_exec()

        return True
