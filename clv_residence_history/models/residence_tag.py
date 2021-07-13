# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResidenceTag(models.Model):
    _inherit = 'clv.residence.tag'

    residence_history_ids = fields.Many2many(
        comodel_name='clv.residence.history',
        relation='clv_residence_history_tag_rel',
        column1='tag_id',
        column2='residence_history_id',
        string='Residences (History)'
    )


class ResidenceHistory(models.Model):
    _inherit = "clv.residence.history"

    tag_ids = fields.Many2many(
        comodel_name='clv.residence.tag',
        relation='clv_residence_history_tag_rel',
        column1='residence_history_id',
        column2='tag_id',
        string='Residence Tags'
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
