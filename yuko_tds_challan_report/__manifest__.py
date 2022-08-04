
{
    'name' : 'Yuko TDS Challan Report',
    'version' : '1.0',
    'author' : 'Odoo Bangladesh',
    'summary': 'Payslip',
    'description': """
            Create Yuko TDS Challan Form Report
    """,
    'category': '',
    'sequence': 6,
    'website' : '',
    'depends' : ["hr_payroll", "amount_to_word_bd",
                 "yuko_report_layout", "report_layout",
                ],
    'data' : ["report/yuko_tds_challan_report_view.xml",
              "views/inherited_payslip_views.xml"],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
