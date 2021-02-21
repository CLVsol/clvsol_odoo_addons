# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    type = fields.Selection(selection_add=[
        ('clv.patient', 'Patient'),
    ])

    patient_ids = fields.One2many(
        string='Related Patients',
        comodel_name='clv.patient',
        compute='_compute_patient_ids_and_count',
    )
    count_patients = fields.Integer(
        compute='_compute_patient_ids_and_count',
    )

    def _get_clv_entity(self):
        self.ensure_one()
        if self.type and self.type[:3] == 'clv':
            return self.env[self.type].search([
                ('partner_id', '=', self.id),
            ])

    def _compute_patient_ids_and_count(self):
        for record in self:
            try:
                patients = self.env['clv.patient'].search([
                    ('partner_id', 'child_of', record.id),
                ])
                record.count_patients = len(patients)
                record.patient_ids = [(6, 0, patients.ids)]
            except TypeError:
                record.count_patients = False
                record.patient_ids = False
