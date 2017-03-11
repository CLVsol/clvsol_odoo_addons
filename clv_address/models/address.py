# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

from lxml import etree

ADDRESS_FORMAT_CLASSES = {
    '%(city)s %(state_code)s\n%(zip)s': 'o_city_state',
    '%(zip)s %(city)s': 'o_zip_city'
}


ADDRESS_FIELDS = ('street', 'street2', 'zip', 'city', 'state_id', 'country_id')


@api.model
def _lang_get(self):
    return self.env['res.lang'].get_installed()


class FormatAddress(object):

    @api.model
    def fields_view_get_address(self, arch):
        address_format = self.env.user.company_id.country_id.address_format or ''
        for format_pattern, format_class in ADDRESS_FORMAT_CLASSES.iteritems():
            if format_pattern in address_format:
                doc = etree.fromstring(arch)
                for address_node in doc.xpath("//div[@class='o_address_format']"):
                    # add address format class to address block
                    address_node.attrib['class'] += ' ' + format_class
                    if format_class.startswith('o_zip'):
                        zip_fields = address_node.xpath("//field[@name='zip']")
                        city_fields = address_node.xpath("//field[@name='city']")
                        if zip_fields and city_fields:
                            # move zip field before city field
                            city_fields[0].addprevious(zip_fields[0])
                arch = etree.tostring(doc)
                break
        return arch


class Address(models.Model, FormatAddress):
    _description = 'Address'
    _name = "clv.address"
    _order = "name"

    name = fields.Char(string='Name', required=True, index=True)

    code = fields.Char(string='Address Code', required=False)

    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street2')
    zip = fields.Char(string='ZIP code', change_default=True)
    city = fields.Char(string='City')
    state_id = fields.Many2one(comodel_name="res.country.state", string='State', ondelete='restrict')
    country_id = fields.Many2one(comodel_name='res.country', string='Country', ondelete='restrict')

    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')
    fax = fields.Char(string='Fax')
    email = fields.Char(string='Email')

    notes = fields.Text(string='Notes')

    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE(code)',
         u'Error! The Address Code must be unique!'
         )
    ]

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        if (not view_id) and (view_type == 'form') and self._context.get('force_email'):
            view_id = self.env.ref('base.view_partner_simple_form').id
        res = super(Address, self).fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu
        )
        if view_type == 'form':
            res['arch'] = self.fields_view_get_address(res['arch'])
        return res

    @api.multi
    def name_get(self):

        res = []
        for address in self:

            # name = address.name
            name = u'%s [%s]' % (address.name, address.code)

            if self._context.get('show_address_only'):
                name = address._display_address()
            if self._context.get('show_address'):
                name = name + "\n" + address._display_address()

            name = name.replace('\n\n', '\n')
            name = name.replace('\n\n', '\n')

            res.append((address.id, name))

        return res

    @api.multi
    def _display_address(self):

        address_format = self.country_id.address_format or \
            "%(street)s\n%(street2)s\n%(city)s %(state_code)s %(zip)s\n%(country_name)s"
        args = {
            'state_code': self.state_id.code or '',
            'state_name': self.state_id.name or '',
            'country_code': self.country_id.code or '',
            'country_name': self.country_id.name or '',
        }
        for field in self._address_fields():
            args[field] = getattr(self, field) or ''
        return address_format % args

    @api.model
    def _address_fields(self):
        """Returns the list of address fields that are synced from the parent."""
        return list(ADDRESS_FIELDS)

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id:
            return {'domain': {'state_id': [('country_id', '=', self.country_id.id)]}}
        else:
            return {'domain': {'state_id': []}}
