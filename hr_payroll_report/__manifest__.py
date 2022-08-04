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
    'name' : 'HR Payslip Report',
    'version' : '1.0',
    'author' : 'Odoo Bangladesh',
    'summary': 'HR',
    'description': """
    
    """,
    'category': 'Human Resources',
    'sequence': 4,
    'website' : '',
    'depends' : ["gbs_hr_payroll", "yuko_hr_employee",'mail',
                 "yuko_report_layout", "l10n_in_hr_payroll",
                 'amount_to_word_bd', 'yuko_report_layout',
                 "gbs_hr_payroll_bank_letter"],
    'data' : ["reports/paperformat.xml",
              "reports/inherit_report_payslip.xml",
              "reports/inherit_payroll_report_view.xml",
              "reports/inherit_yearly_salary_detail_template.xml",
              "views/hr_payslip_data.xml",
              'views/inherit_hr_payroll_views.xml',
              'views/hr_payslip_run_view.xml',],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
