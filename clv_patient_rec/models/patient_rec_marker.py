# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PatientMarker(models.Model):
    _inherit = 'clv.patient.marker'

    patient_rec_ids = fields.Many2many(
        comodel_name='clv.patient_rec',
        relation='clv_patient_rec_marker_rel',
        column1='marker_id',
        column2='patient_rec_id',
        string='Patients (Rec)'
    )


class PatientRec(models.Model):
    _inherit = "clv.patient_rec"

    marker_ids = fields.Many2many(
        comodel_name='clv.patient.marker',
        relation='clv_patient_rec_marker_rel',
        column1='patient_rec_id',
        column2='marker_id',
        string='Markers'
    )
    marker_names = fields.Char(
        string='Marker Names',
        compute='_compute_marker_names',
        store=True
    )

    @api.depends('marker_ids')
    def _compute_marker_names(self):
        for r in self:
            marker_names = False
            for marker in r.marker_ids:
                if marker_names is False:
                    marker_names = marker.name
                else:
                    marker_names = marker_names + ', ' + marker.name
            r.marker_names = marker_names
