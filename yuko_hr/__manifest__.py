# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
    'name' : 'YUKO HR',
    'version' : '1.0',
    'author' : 'Odoo Bangladesh',
    'summary': 'HR',
    'description': """
    
    """,
    'category': 'Human Resources',
    'sequence': 4,
    'website' : '',
    'depends' : ['hr',
                 'calendar',
                 'hr_payroll', 'base', 'hr_recruitment',
                 'hr_employee_age',
                 'hr_employee_blood_group',
                 'hr_employee_operating_unit',
                 'get_org_chart',
                 'hr_manual_attendance',
                 'gbs_hr_public_holidays',
                 'hr_payslip_monthly_report',
                 'l10n_in_hr_payroll',
                 'gbs_hr_payroll',
                 'hr_appraisal',
                 'report_layout',],

    'data' : [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/menu_access_view.xml',
        "views/menu.xml",
        'views/inherit_hr_appraisal_views.xml',
        'views/inherit_hr_payroll_views.xml',
        "reports/inherit_provident_fund_template_view.xml",
         'views/hr_employee_view.xml',
    ],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
