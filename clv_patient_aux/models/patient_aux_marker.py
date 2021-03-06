# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PatientMarker(models.Model):
    _inherit = 'clv.patient.marker'

    patient_aux_ids = fields.Many2many(
        comodel_name='clv.patient_aux',
        relation='clv_patient_aux_marker_rel',
        column1='marker_id',
        column2='patient_aux_id',
        string='Patients (Aux)'
    )


class PatientAux(models.Model):
    _inherit = "clv.patient_aux"

    marker_ids = fields.Many2many(
        comodel_name='clv.patient.marker',
        relation='clv_patient_aux_marker_rel',
        column1='patient_aux_id',
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
