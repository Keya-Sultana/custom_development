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
    'name' : 'Yuko HR Employee',
    'version' : '1.0',
    'author' : 'Odoo Bangladesh',
    'summary': 'HR',
    'description': """
    
    """,
    'category': 'Human Resources',
    'sequence': 4,
    'website' : '',
    'depends' : ["hr",
                 'gbs_hr_employee',
                 'gbs_hr_payroll',
                 'hr_employee_academic',
                 # 'hr_employee_bank',
                 'hr_employee_children',
                 'hr_employee_content',
                 'hr_employee_family',
                 'hr_employee_nick_name',
                 'hr_employee_seniority',
                 'hr_employee_specialization',
                 'hr_employee_training',
                 'hr_attendance',
                 'hr_manual_attendance',
                 'hr_employee_id',
                 'hr_employee_exit',],
    'data' : ["views/hr_employee_view.xml",
              'views/inherit_hr_payslip_run_views.xml',
              'views/hr_employee_kanban_view.xml',
              'views/final_settlement_view.xml',
              'reports/final_settlement_report.xml',
              ],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
