# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class FamilyOff(models.Model):
    _inherit = 'clv.family_off'

    person_off_ids = fields.One2many(
        comodel_name='clv.person_off',
        inverse_name='family_off_id',
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

    family_off_id = fields.Many2one(comodel_name='clv.family_off', string='Family (Off)', ondelete='restrict')
    family_off_code = fields.Char(string='Family (Off) Code', related='family_off_id.code', store=False)

    family_off_category_ids = fields.Char(
        string='Family (Off) Categories',
        related='family_off_id.category_ids.name',
        store=True
    )
