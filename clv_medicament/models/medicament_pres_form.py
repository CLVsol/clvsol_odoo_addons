# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import api, fields, models


class MedicamentPresentationForm(models.Model):
    _description = 'Medicament Presentation Form'
    _name = 'clv.medicament.pres_form'
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'

    name = fields.Char(
        string='Presentation Form', required=True,
        translate=True,
        help='Medicament Presentation Form.'
    )

    code = fields.Char(string='Code')

    description = fields.Char(string='Description')

    notes = fields.Text(string='Notes')

    active = fields.Boolean(string='Active', default=1)

    parent_id = fields.Many2one(
        comodel_name='clv.medicament.pres_form',
        string='Parent Form',
        index=True,
        ondelete='restrict'
    )
    child_ids = fields.One2many(
        comodel_name='clv.medicament.pres_form',
        inverse_name='parent_id',
        string='Child Forms'
    )
    complete_name = fields.Char(
        string='Full Presentation Form',
        compute='_name_get_fnc',
        store=False,
        readonly=True
    )
    parent_left = fields.Integer(string='Left parent', index=True)
    parent_right = fields.Integer(string='Right parent', index=True)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         u'Error! The Presentation Form must be unique!'),
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]

    _constraints = [
        (models.Model._check_recursion,
         'Error! You can not create recursive presentation forms.',
         ['parent_id']),
    ]

    @api.multi
    def name_get(self):
        """Return the form's display name, including their direct parent by default.

        :param dict context: the ``pres_form_display`` key can be
                             used to select the short version of the
                             form (without the direct parent),
                             when set to ``'short'``. The default is
                             the long version."""
        if self._context is None:
            self._context = {}
        if self._context.get('pres_form_display') == 'short':
            return super(MedicamentPresentationForm, self).name_get()
        if isinstance(self._ids, (int, long)):
            self._ids = [self._ids]
        reads = self.read(['name', 'parent_id'])
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1] + ' / ' + name
            res.append((record['id'], name))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        categories = self.search(args, limit=limit)
        return categories.name_get()

    @api.one
    def _name_get_fnc(self):
        self.refresh_complete_name = 0
        complete_name = self.name_get()
        if complete_name:
            self.complete_name = complete_name[0][1]
        else:
            self.complete_name = self.name
