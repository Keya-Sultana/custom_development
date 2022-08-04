{
    'name': 'HR OverTime Requisition',
    'summary': 'This Module is use for OverTime Requisition.',
    'author':  'Odoo Bangladesh',
    'website': 'www.odoo.com.bd',
    'category': 'HR Attendance',
    'version': "15.0.1.0.0",
    'license': 'LGPL-3',
    'depends': [
        'hr',
        'hr_attendance',
        'resource',
        'operating_unit',
        # There is dependency on hr_holidays_multi_levels_approval, but for temporary blocking the dependency
        # 'hr_holidays_multi_levels_approval',
        # 'gbs_application_group',
        ],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        # 'views/hr_overtime_requisition_view.xml'
    ],
    'installable': True,
    'application': True,
}