# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Family(models.Model):
    _inherit = 'clv.family'

    person_off_ids = fields.One2many(
        comodel_name='clv.person_off',
        inverse_name='family_id',
        string='Persons (Off)'
    )
    count_person_offs = fields.Integer(
        string='Persons (Off) (count)',
        compute='_compute_count_person_offs',
        store=True
    )

    @api.depends('person_off_ids')
    def _compute_count_person_offs(self):
        for r in self:
            r.count_person_offs = len(r.person_off_ids)


class PersonOff(models.Model):
    _inherit = 'clv.person_off'

    family_id = fields.Many2one(comodel_name='clv.family', string='Family', ondelete='restrict')
    family_code = fields.Char(string='Family Code', related='family_id.code', store=False)

    family_category_ids = fields.Char(
        string='Family Categories',
        related='family_id.category_ids.name',
        store=True
    )
