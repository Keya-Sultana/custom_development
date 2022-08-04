
{
    'name' : 'Yuko Maternity Report',
    'version' : '1.0',
    'author' : 'Odoo Bangladesh',
    'summary': 'Payslip',
    'description': """
                Create Yuko Maternity Benefit Bill Report
    """,
    'category': '',
    'sequence': 5,
    'website' : '',
    'depends' : ["hr_payroll",
                 "yuko_report_layout",
                ],
    'data' : [
        "report/yuko_maternity_report_view.xml",
        "views/inherited_payslips_views.xml",
    ],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
