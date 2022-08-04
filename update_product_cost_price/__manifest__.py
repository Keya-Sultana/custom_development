# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2010-2014 Elico Corp. All Rights Reserved.
#    Augustin Cisterne-Kaas <augustin.cisterne-kaas@elico-corp.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Updating Product Cost Price',
    'version': '0.1',
    'category': 'Warehouse',
    'depends': ['product'],
    'author': 'Odoo Bangladesh',
    'license': 'AGPL-3',
    'website': 'https://www.odoo.com.bd',
    'description': """
        Module which able to update product cost price.
    """,
    'data': ["views/cost_price_update_view.xml",
             #"security/ir.model.access.csv",
             ],
    'installable': True,
    'application': False,
}
