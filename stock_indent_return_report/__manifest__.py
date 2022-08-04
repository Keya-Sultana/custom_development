# -*- coding: utf-8 -*-
{
    'name': "Stock Indent Return Report",

    'summary': """
        Custom Report Of Return Product""",

    'description': """
        By this report user can get the record of 
        return product list by departmental and periodical.
    """,

    'author': "Odoo Bangladesh",

    'category': 'Stock',
    'version': '1.0',

    'depends': ['indent_return','report_layout'],

     'data': [
    #     'security/ir.model.access.csv',
        'report/stock_return_report.xml',
        'wizard/stock_return_wizard.xml',

    ],

}