# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name': 'EPC HR',
    'version': '1.0.0',
    'category': 'Logo',
    "sequence": 1,
    'summary': 'HR',
    'complexity': "easy",
    "author": "Odoo Bangladesh",
    "website": "http://www.odoo.com.bd",
    'depends': ['hr','hr_contract', 'hr_attendance', 'web'],
    'data': ['views/inherit_hr_employee_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
