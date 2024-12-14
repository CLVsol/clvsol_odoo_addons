# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    type = fields.Selection(selection_add=[
        ('clv.patient_rec', 'Patient (Rec)'),
    ])

    patient_rec_ids = fields.One2many(
        string='Related Patients (Rec)',
        comodel_name='clv.patient_rec',
        compute='_compute_patient_rec_ids_and_count',
    )
    count_patients_rec = fields.Integer(
        compute='_compute_patient_rec_ids_and_count',
    )

    def _get_clv_entity(self):
        self.ensure_one()
        if self.type and self.type[:3] == 'clv':
            return self.env[self.type].search([
                ('partner_id', '=', self.id),
            ])

    def _compute_patient_rec_ids_and_count(self):
        for record in self:
            try:
                patients_rec = self.env['clv.patient_rec'].search([
                    ('partner_id', 'child_of', record.id),
                ])
                record.count_patients_rec = len(patients_rec)
                record.patient_rec_ids = [(6, 0, patients_rec.ids)]
            except TypeError:
                record.count_patients_rec = False
                record.patient_rec_ids = False
