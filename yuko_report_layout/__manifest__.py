{
    'name': 'Yuko Report Layout',
    'category': 'Reprot',
    'summary': 'Add custom header and footer',
    'author': 'Odoo Bangladesh',
    'depends': ['web','report'],
    'data': [
        'views/report_layout.xml',
        'views/internal_layout.xml',
        "views/bank_layout.xml",
        "views/attendance_layout.xml",
        "views/purchase_order_layout.xml",
        "views/stockpicking_operation_bercode.xml",
        "views/payslip_summary_layout.xml",
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
