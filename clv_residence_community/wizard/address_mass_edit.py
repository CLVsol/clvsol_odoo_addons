# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AddressMassEdit(models.TransientModel):
    _inherit = 'clv.address.mass_edit'

    is_residence = fields.Boolean(
        string='Is Residence'
    )
    is_residence_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Is Residence:', default=False, readonly=False, required=False
    )

    def do_address_mass_edit(self):
        self.ensure_one()

        super().do_address_mass_edit()

        for address in self.address_ids:

            _logger.info(u'%s %s', '>>>>>', address.name)

            if self.is_residence_selection == 'set':
                address.is_residence = self.is_residence
            if self.is_residence_selection == 'remove':
                address.is_residence = False

        return True
