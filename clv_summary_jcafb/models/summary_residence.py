# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SummaryResidence(models.Model):
    _description = 'Summary Residence'
    _name = 'clv.summary.residence'

    summary_id = fields.Many2one(
        comodel_name='clv.summary',
        string='Summary',
        index=True,
        ondelete='cascade'
    )
    residence_id = fields.Many2one(
        comodel_name='clv.residence',
        string='Residence',
        ondelete='cascade'
    )
    residence_global_tag_ids = fields.Many2many(
        string='Residence Global Tags',
        related='residence_id.global_tag_ids',
        store=False
    )
    residence_category_ids = fields.Many2many(
        string='Residence Categories',
        related='residence_id.category_ids',
        store=False
    )
    residence_state = fields.Selection(
        string='Residence State',
        related='residence_id.state',
        store=False
    )
    residence_phase_id = fields.Many2one(
        string='Residence Phase',
        related='residence_id.phase_id',
        store=False
    )


class Summary(models.Model):
    _inherit = "clv.summary"

    summary_residence_ids = fields.One2many(
        comodel_name='clv.summary.residence',
        inverse_name='summary_id',
        string='Residences'
    )
