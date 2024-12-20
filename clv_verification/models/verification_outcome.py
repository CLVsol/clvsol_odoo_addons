# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):

    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class VerificationOutcome(models.Model):
    _description = 'Verification Outcome'
    _name = 'clv.verification.outcome'
    _order = "id desc"
    _rec_name = 'reference_name'

    date_verification = fields.Datetime(string="Verification Date")
    state = fields.Selection(
        [('Error (L0)', 'Error (L0)'),
         ('Warning (L0)', 'Warning (L0)'),
         ('Error (L1)', 'Error (L1)'),
         ('Warning (L1)', 'Warning (L1)'),
         ('Error (L2)', 'Error (L2)'),
         ('Warning (L2)', 'Warning (L2)'),
         ('Ok', 'Ok'),
         ('Updated', 'Updated'),
         ('Unknown', 'Unknown'),
         ('Missing', 'Missing'),
         ], string='State', default='Unknown'
    )
    outcome_info = fields.Text(string='Outcome Informations')

    model = fields.Char(string='Model Name ', required=True)
    res_id = fields.Integer(
        string='Record ID',
        help="ID of the target record in the database",
        required=True
    )
    res_last_update = fields.Datetime(string="Record Last Update")
    reference = fields.Char(
        string='Reference ',
        compute='_compute_reference',
        readonly=True,
        store=True
    )
    reference_name = fields.Char(
        string='Reference Name',
        compute='_compute_reference',
        readonly=True,
        store=True
    )

    action = fields.Char(
        string='Action',
        required=False,
        help="Name of the action used to process the verification."
    )

    active = fields.Boolean(string='Active', default=1)

    @api.depends('model', 'res_id')
    def _compute_reference(self):
        for record in self:
            record.reference = False
            record.reference_name = False
            if (record.model is not False) and (record.res_id != 0):
                record.reference = "%s,%s" % (record.model, record.res_id)
                Model = self.env[record.model]
                rec = Model.search([
                    ('id', '=', record.res_id),
                ])
                if rec.name_get() != []:
                    record.reference_name = rec.name_get()[0][1]

    def _get_verification_outcome_state(self, current_state, new_state):

        verification_state = current_state

        if new_state == 'Error (L0)':
            verification_state = 'Error (L0)'
        elif (new_state == 'Warning (L0)') and \
             (current_state not in ['Error (L0)']):
            verification_state = 'Warning (L0)'
        elif (new_state == 'Error (L1)') and \
             (current_state not in ['Warning (L0)', 'Error (L0)']):
            verification_state = 'Error (L1)'
        elif (new_state == 'Warning (L1)') and \
             (current_state not in ['Error (L1)', 'Warning (L0)', 'Error (L0)']):
            verification_state = 'Warning (L1)'
        elif (new_state == 'Error (L2)') and \
             (current_state not in ['Warning (L1)', 'Error (L1)', 'Warning (L0)', 'Error (L0)']):
            verification_state = 'Error (L2)'
        elif (new_state == 'Warning (L2)') and \
             (current_state not in ['Error (L2)', 'Warning (L1)', 'Error (L1)', 'Warning (L0)', 'Error (L0)']):
            verification_state = 'Warning (L2)'
        elif (new_state == 'Ok') and \
             (current_state not in ['Warning (L2)', 'Error (L2)', 'Warning (L1)', 'Error (L1)',
                                    'Warning (L0)', 'Error (L0)']):
            verification_state = 'Ok'
        elif (new_state not in ['Ok', 'Warning (L2)', 'Error (L2)', 'Warning (L1)', 'Error (L1)',
                                'Warning (L0)', 'Error (L0)']):
            verification_state = new_state

        return verification_state

    def _object_verification_outcome_model_object_verification_state_updt(self, model_object):

        _logger.info(u'%s %s -> %s', '>>>>>>>>>>>>>>>>>>>>',
                     model_object, model_object.verification_outcome_ids)

        verification_state = 'Unknown'
        for verification_outcome in model_object.verification_outcome_ids:
            verification_state = self._get_verification_outcome_state(verification_state,
                                                                      verification_outcome.state)
        if model_object.verification_state != verification_state:
            model_object.verification_state = verification_state

    def _object_verification_outcome_updt(
        self, verification_outcome, state, outcome_info, date_verification, model_object
    ):

        verification_values = {}
        verification_values['date_verification'] = date_verification
        verification_values['outcome_info'] = outcome_info
        verification_values['state'] = state
        verification_outcome.write(verification_values)
