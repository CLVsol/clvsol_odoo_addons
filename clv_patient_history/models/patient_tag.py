# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PatientTag(models.Model):
    _inherit = 'clv.patient.tag'

    patient_history_ids = fields.Many2many(
        comodel_name='clv.patient.history',
        relation='clv_patient_history_tag_rel',
        column1='tag_id',
        column2='patient_history_id',
        string='Patients (History)'
    )


class PatientHistory(models.Model):
    _inherit = "clv.patient.history"

    tag_ids = fields.Many2many(
        comodel_name='clv.patient.tag',
        relation='clv_patient_history_tag_rel',
        column1='patient_history_id',
        column2='tag_id',
        string='Patient Tags'
    )
    tag_names = fields.Char(
        string='Tag Names',
        compute='_compute_tag_names',
        store=True
    )

    @api.depends('tag_ids')
    def _compute_tag_names(self):
        for r in self:
            tag_names = False
            for tag in r.tag_ids:
                if tag_names is False:
                    tag_names = tag.name
                else:
                    tag_names = tag_names + ', ' + tag.name
            r.tag_names = tag_names
