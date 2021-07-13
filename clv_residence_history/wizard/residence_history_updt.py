# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models
from odoo import exceptions

_logger = logging.getLogger(__name__)


class ResidenceHistoryUpdate(models.TransientModel):
    _description = 'Residence History Update'
    _name = 'clv.residence.history_updt'

    def _default_residence_ids(self):
        return self._context.get('active_ids')
    residence_ids = fields.Many2many(
        comodel_name='clv.residence',
        relation='residence_history_updt_rel',
        string='Residences',
        default=_default_residence_ids
    )
    date_sign_in = fields.Date(
        string='Sign in date',
        required=False,
    )
    date_sign_out = fields.Date(
        string="Sign out date",
        required=False
    )

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

    def do_residence_history_updt(self):
        self.ensure_one()

        ResidenceHistory = self.env['clv.residence.history']

        for residence in self.residence_ids:

            if self.date_sign_out is False:
                raise exceptions.ValidationError('The "Sign out date" has not been defined!')
                return self._reopen_form()

            if self.date_sign_in is False:
                raise exceptions.ValidationError('The "Sign in date" has not been defined!')
                return self._reopen_form()

            _logger.info(u'%s %s', '>>>>>', residence.name)

            if residence.phase_id.id is not False:

                residence_history = ResidenceHistory.search([
                    ('residence_id', '=', residence.id),
                    ('phase_id', '=', residence.phase_id.id),
                    ('date_sign_out', '=', False),
                ])

                if residence_history.id is False:

                    residence_history_2 = ResidenceHistory.search([
                        ('residence_id', '=', residence.id),
                        ('date_sign_out', '=', False),
                    ])
                    if residence_history_2.id is not False:
                        residence_history_2.date_sign_out = self.date_sign_out
                        _logger.info(u'%s %s %s %s', '>>>>>>>>>>', residence_history_2.phase_id.name,
                                                     residence_history_2.date_sign_in,
                                                     residence_history_2.date_sign_out)

                    m2m_list = []
                    for category_id in residence.category_ids:
                        m2m_list.append((4, category_id.id))
                    category_ids = m2m_list
                    m2m_list = []
                    for marker_id in residence.marker_ids:
                        m2m_list.append((4, marker_id.id))
                    marker_ids = m2m_list
                    m2m_list = []
                    for tag_id in residence.tag_ids:
                        m2m_list.append((4, tag_id.id))
                    tag_ids = m2m_list
                    values = {
                        'phase_id': residence.phase_id.id,
                        'date_sign_in': self.date_sign_in,
                        'state': residence.state,
                        'reg_state': residence.reg_state,
                        'employee_id': residence.employee_id.id,
                        'residence_id': residence.id,
                        'category_ids': category_ids,
                        'marker_ids': marker_ids,
                        'tag_ids': tag_ids,
                    }
                    residence_history = ResidenceHistory.create(values)
                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', residence_history.phase_id.name,
                                                 residence_history.date_sign_in,
                                                 residence_history.date_sign_out)

                else:

                    if residence_history.state != residence.state:
                        residence_history.state = residence.state

                    if residence_history.reg_state != residence.reg_state:
                        residence_history.reg_state = residence.reg_state

                    if residence_history.employee_id.id != residence.employee_id.id:
                        residence_history.employee_id = residence.employee_id.id

                    m2m_list = []
                    for category_id in residence.category_ids:
                        m2m_list.append((4, category_id.id))
                    m2m_list_2 = []
                    for category_id in residence_history.category_ids:
                        m2m_list_2.append((4, category_id.id))
                    if m2m_list != m2m_list_2:
                        residence_history.category_ids = m2m_list

                    m2m_list = []
                    for marker_id in residence.marker_ids:
                        m2m_list.append((4, marker_id.id))
                    m2m_list_2 = []
                    for marker_id in residence_history.marker_ids:
                        m2m_list_2.append((4, marker_id.id))
                    if m2m_list != m2m_list_2:
                        residence_history.marker_ids = m2m_list

                    m2m_list = []
                    for tag_id in residence.tag_ids:
                        m2m_list.append((4, tag_id.id))
                    m2m_list_2 = []
                    for tag_id in residence_history.tag_ids:
                        m2m_list_2.append((4, tag_id.id))
                    if m2m_list != m2m_list_2:
                        residence_history.tag_ids = m2m_list

                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', residence_history.phase_id.name,
                                                 residence_history.date_sign_in,
                                                 residence_history.date_sign_out)

            else:

                residence_history = ResidenceHistory.search([
                    ('residence_id', '=', residence.id),
                    ('date_sign_out', '=', False),
                ])

                if residence_history.id is not False:
                    residence_history.date_sign_out = self.date_sign_out
                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', residence_history.phase_id.name,
                                                 residence_history.date_sign_in,
                                                 residence_history.date_sign_out)

        return True
        # return self._reopen_form()
