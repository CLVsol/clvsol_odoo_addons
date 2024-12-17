# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Patient(models.Model):
    _inherit = 'clv.patient'

    event_attendee_ids = fields.One2many(
        string='Event Attendees',
        comodel_name='clv.event.attendee',
        compute='_compute_event_attendee_ids_and_count',
    )
    count_events = fields.Integer(
        string='Events (count)',
        compute='_compute_event_attendee_ids_and_count',
    )
    count_events_2 = fields.Integer(
        string='Events 2 (count)',
        compute='_compute_event_attendee_ids_and_count',
    )

    def _compute_event_attendee_ids_and_count(self):
        for record in self:

            search_domain = [
                ('ref_id', '=', self._name + ',' + str(record.id)),
            ]
            event_attendees_2 = self.env['clv.event.attendee'].search(search_domain)

            if record.phase_id.id is not False:
                search_domain.append(
                    ('event_phase_id.id', '=', record.phase_id.id),
                )
            event_attendees = self.env['clv.event.attendee'].search(search_domain)

            record.count_events = len(event_attendees)
            record.count_events_2 = len(event_attendees_2)
            record.event_attendee_ids = [(6, 0, event_attendees.ids)]
