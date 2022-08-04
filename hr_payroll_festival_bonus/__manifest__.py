{
    'name': 'HR Payroll Festival Bonus',
    'author': 'Odoo Bangladesh',
    'website': 'www.odoo.com.bd',
    'category': 'HR Payroll',
    'version': "15.0.1.0.0",
    'depends': [
        'hr_payroll',
        ],
    'data': [
        'data/data.xml',
        'views/inherited_hr_payslip.xml',
        #'views/inherit_hr_contract.xml',
    ],

    'summary': 'This Module Generate Payroll Festival Bonus Summary',
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}