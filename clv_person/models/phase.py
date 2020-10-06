# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Phase(models.Model):
    _inherit = 'clv.phase'

    person_ids = fields.One2many(
        comodel_name='clv.person',
        inverse_name='phase_id',
        string='Persons',
        readonly=True
    )
    count_persons = fields.Integer(
        string='Persons (count)',
        compute='_compute_person_ids_and_count',
    )

    def _compute_person_ids_and_count(self):
        for record in self:

            search_domain = [
                ('phase_id', '=', record.id),
            ]

            persons = self.env['clv.person'].search(search_domain)

            record.count_persons = len(persons)
            record.person_ids = [(6, 0, persons.ids)]


class Person(models.Model):
    _inherit = 'clv.person'

    phase_id = fields.Many2one(
        comodel_name='clv.phase',
        string='Phase',
        ondelete='restrict'
    )
