# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Phase(models.Model):
    _inherit = 'clv.phase'

    person_history_ids = fields.One2many(
        comodel_name='clv.person.history',
        inverse_name='phase_id',
        string='Persons (History)',
        readonly=True
    )
    count_person_histories = fields.Integer(
        string='Persons (History) (count)',
        compute='_compute_person_history_ids_and_count',
    )

    def _compute_person_history_ids_and_count(self):
        for record in self:

            search_domain = [
                ('phase_id', '=', record.id),
            ]

            person_histories = self.env['clv.person.history'].search(search_domain)

            record.count_person_histories = len(person_histories)
            record.person_history_ids = [(6, 0, person_histories.ids)]


class PersonHistory(models.Model):
    _inherit = 'clv.person.history'

    phase_id = fields.Many2one(
        comodel_name='clv.phase',
        string='Phase',
        ondelete='restrict'
    )
