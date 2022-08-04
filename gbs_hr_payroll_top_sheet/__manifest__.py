{
    'name': 'GBS HR Payroll Top Sheet',
    'author': 'Odoo Bangladesh',
    'website': 'www.odoo.com.bd',
    'category': 'payroll',
    'version': "15.0.1.0.0",
    'license': 'LGPL-3',
    'depends': [
        # 'web.report_layout',
        'web',
        'gbs_hr_attendance_report',
        # 'amount_to_word_bd',
        'gbs_hr_payroll',
        # 'hr_payroll',
    ],
    'data': [
        'report/payroll_top_sheet_report_view.xml',

    ],
    'summary': '',
    'description': " This module shows monthly employee's salary top sheet report",
    'installable': True,
    'application': True,
}
