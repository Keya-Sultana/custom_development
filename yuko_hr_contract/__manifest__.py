{
    'name' : 'YUKO HR Contracts',
    'version' : '1.0',
    'author' : 'Odoo Bangladesh',
    'summary': 'HR',
    'description': """
    
    """,
    'category': 'Human Resources',
    'sequence': 4,
    'website' : '',
    'depends' : ['hr',
                 'hr_employee_attendance_payroll',
                 'hr_contract',
                 'report',
                 'gbs_hr_payroll',],

    'data' : [
            'security/ir.model.access.csv',
            'report/paperformat.xml',
            'report/salary_increment_letter_report_view.xml',
            'report/job_confirmation_letter_report_view.xml',
            "report/employee_contract_report_view.xml",
            "views/inherit_hr_contract_views.xml",
            ],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
