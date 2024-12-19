# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SummaryPatient(models.Model):
    _description = 'Summary Patient'
    _name = 'clv.summary.patient'

    summary_id = fields.Many2one(
        comodel_name='clv.summary',
        string='Summary',
        index=True,
        ondelete='cascade'
    )
    patient_id = fields.Many2one(
        comodel_name='clv.patient',
        string='Patient',
        ondelete='cascade'
    )
    patient_gender = fields.Selection(
        string='Patient Gender',
        related='patient_id.gender',
        store=False
    )
    patient_birthday = fields.Date(
        string='Patient Date of Birth',
        related='patient_id.birthday',
        store=False
    )
    patient_global_tag_ids = fields.Many2many(
        string='Patient Global Tags',
        related='patient_id.global_tag_ids',
        store=False
    )
    patient_category_ids = fields.Many2many(
        string='Patient Categories',
        related='patient_id.category_ids',
        store=False
    )
    patient_state = fields.Selection(
        string='Patient State',
        related='patient_id.state',
        store=False
    )
    patient_phase_id = fields.Many2one(
        string='Patient Phase',
        related='patient_id.phase_id',
        store=False
    )


class Summary(models.Model):
    _inherit = "clv.summary"

    summary_patient_ids = fields.One2many(
        comodel_name='clv.summary.patient',
        inverse_name='summary_id',
        string='Patients'
    )
