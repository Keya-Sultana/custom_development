# -*- coding: utf-8 -*-

###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Sreejith P(<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

{
    'name': 'Product Barcode Generator',
    'version' : '1.0',
    'summary': 'Generates EAN13 Standard Barcode for Product.',
    'category': 'Inventory',
    'author': 'Odoo Bangladesh Limited',
    'maintainer': 'Odoo Bangladesh Limited',
    'company': 'Odoo Bangladesh Limited',
    'website': 'http://www.odoo.com.bd',
    'depends': ['product','web'],
    'data': [
        'views/paperformat.xml',
        'views/product_label.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
