# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class ModelExport(models.Model):
    _inherit = 'clv.model_export'

    export_patient_ids = fields.Many2many(
        comodel_name='clv.patient',
        relation='clv_export_patient_rel',
        column1='patient_id',
        column2='export_id',
        string='Export Patients'
    )
    count_export_patients = fields.Integer(
        string='Patients (count)',
        compute='_compute_count_export_patients',
        store=True
    )

    @api.depends('export_patient_ids')
    def _compute_count_export_patients(self):
        for r in self:
            r.count_export_patients = len(r.export_patient_ids)

    @api.depends('model_model')
    def compute_model_items(self):
        for r in self:
            r.model_items = False
            if self.model_model == 'clv.patient':
                r.model_items = 'export_patient_ids'
        super().compute_model_items()


class ModelExport_xls(models.Model):
    _inherit = 'clv.model_export'

    def do_model_export_execute_xls_patient(self):

        self.do_model_export_execute_xls()


class ModelExport_csv(models.Model):
    _inherit = 'clv.model_export'

    def do_model_export_execute_csv_patient(self):

        self.do_model_export_execute_csv()


class ModelExport_sqlite(models.Model):
    _inherit = 'clv.model_export'

    def do_model_export_execute_sqlite_patient(self):

        self.do_model_export_execute_sqlite()
