# -*- coding: utf-8 -*-
{
    'name': "Offence Integration With Payroll",
    'author': "Odoo Bangladesh",
    'category': 'Human Resources',
    'website': "",
    'summary': """
        This module integrate employees monthly mobile bill with payroll.""",
    'description': """
        This module integrate employees monthly mobile bill with payroll.
    """,
    "depends": [
         'hr',
        'hr_payroll',
        'l10n_in_hr_payroll',
        'hr_employee_offence'
    ],
    'data': [
        #'views/inherited_hr_payslip_views.xml'
    ],
    'application': False,
}
