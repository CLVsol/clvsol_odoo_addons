# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PersonAssociateToPersonOff(models.TransientModel):
    _description = 'Person Associate to Person (Off)'
    _name = 'clv.person.associate_to_person_off'

    def _default_person_ids(self):
        return self._context.get('active_ids')
    person_ids = fields.Many2many(
        comodel_name='clv.person',
        relation='clv_person_associate_to_person_off_rel',
        string='Persons',
        default=_default_person_ids
    )

    create_new_person_off = fields.Boolean(
        string='Create new Person (Off)',
        default=True,
        readonly=True
    )

    @api.multi
    def _reopen_form(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
        return action

    @api.multi
    def do_person_associate_to_person_off(self):
        self.ensure_one()

        person_count = 0
        for person in self.person_ids:

            person_count += 1

            _logger.info(u'%s %s %s', '>>>>>', person_count, person.name)

            PersonOff = self.env['clv.person_off']
            person_off = PersonOff.search([
                ('related_person_id', '=', person.id),
            ])
            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'person_off_id:', person_off.id)

            if person_off.id is not False:

                new_person_off = person_off

            else:

                if self.create_new_person_off:

                    values = {}
                    values['name'] = person.name

                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                    new_person_off = PersonOff.create(values)
                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'new_person_off:', new_person_off)

                    values = {}
                    values['related_person_id'] = person.id
                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                    new_person_off.write(values)

                    new_person_off.do_person_off_get_related_person_data()

        if person_count == 1:

            action = {
                'type': 'ir.actions.act_window',
                'name': 'Persons (Off)',
                'res_model': 'clv.person_off',
                'res_id': new_person_off.id,
                'view_type': 'form',
                'view_mode': 'tree,kanban,form',
                'target': 'current',
                'context': {'search_default_name': new_person_off.name},
            }

        else:

            action = {
                'type': 'ir.actions.act_window',
                'name': 'Persons (Off)',
                'res_model': 'clv.person_off',
                'view_type': 'form',
                'view_mode': 'tree,kanban,form',
                'target': 'current',
            }

        return action
        # return True
