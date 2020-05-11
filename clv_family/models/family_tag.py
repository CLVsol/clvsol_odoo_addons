# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class FamilyTag(models.Model):
    _description = 'Family Tag'
    _name = 'clv.family.tag'
    _inherit = 'clv.abstract.tag'

    code = fields.Char(string='Tag Code', required=False)

    family_ids = fields.Many2many(
        comodel_name='clv.family',
        relation='clv_family_tag_rel',
        column1='tag_id',
        column2='family_id',
        string='Families'
    )


class Family(models.Model):
    _inherit = "clv.family"

    tag_ids = fields.Many2many(
        comodel_name='clv.family.tag',
        relation='clv_family_tag_rel',
        column1='family_id',
        column2='tag_id',
        string='Family Tags'
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
