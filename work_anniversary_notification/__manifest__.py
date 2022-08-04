# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<http://www.cybrosys.com>).
#    Author: Sreejith P(<http://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Work Anniversary Notification',
    'version': '10.0.1.0.0',
    'summary': 'This module will wish the employees on their work anniversary.',
    'category': 'Human Resource',
    'sequence': 55,
    'author': 'Odoo Bangladesh',
    'company': 'Odoo Bangladesh',
    'website': 'http://www.odoo.com.bd',
    'depends': ['hr','hr_employee_seniority'],
    'data': ['data/email.xml'],
    'test': [],
    'license': 'AGPL-3',
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
}

