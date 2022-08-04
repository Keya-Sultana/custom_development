# -*- coding: utf-8 -*-
{
    'name': 'Accounting Reports',
    'summary': 'Customized Accounting Report.',
    'description': """
Accounting Reports
====================
    """,
    "author": "Odoo Bangladesh Limited",
    "website": "http://www.odoo.com.bd",
    'version': '10.0.0.1',
    'category': 'Accounting',
    'depends': ['base', 'account_reports'],
    'data': [
        'data/inherit_account_financial_report_data.xml',
    ],
    'installable': True,
    'application': False,
}
