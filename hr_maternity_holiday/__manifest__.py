# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Bangladesh Limited
#    Copyright (C) 2017-TODAY Odoo Bangladesh (<http://www.odoo.com.bd>).

#    You can modify it under the terms of the GNU LESSER
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
    'name': 'Maternity Leave Management',
    'version': '10.0.1.0.0',
    'summary': 'Holidays, Allocation and Leave Requests',
    'category': 'Human Resource',
    'sequence': 55,
    'author': 'Odoo Bangladesh',
    'company': 'Odoo Bangladesh',
    'website': 'http://www.odoo.com.bd',
    'depends': ["base",
                'hr_holidays',
                'hr_payroll',
                "amount_to_word_bd",
                'yuko_report_layout',
                'gbs_application_group',],
    'data': ['security/ir.model.access.csv',
             'data/hr_maternity_holidays_data.xml',
             'report/maternity leave_report_view.xml',
             "views/maternity_template_views.xml",
             "views/maternity_holiday_view.xml",],
    'test': [],
    'license': 'AGPL-3',
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
}

