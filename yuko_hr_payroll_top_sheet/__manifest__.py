{
    'name': 'Yuko HR Payroll Top Sheet',
    'author': 'Odoo Bangladesh',
    'category': 'Human Resources',
    'version': '10.0.1.0.0',
    'depends': [
        'yuko_report_layout', 'report',
        'amount_to_word_bd', 'gbs_hr_payroll_top_sheet',
        'gbs_hr_payroll',
    ],
    'data': [
        'report/inherit_payroll_top_sheet_report.xml',

    ],
    'summary': '',
    'description':" This module shows monthly emplyee's salary top sheet report",
    'installable': True,
    'application': True,
}
