

{
    'name' : 'YUKO HR Attendance',
    'version' : '1.0',
    'author' : 'Odoo Bangladesh',
    'summary': 'HR',
    'description': """
    
    """,
    'category': 'Human Resources',
    'sequence': 4,
    'website' : '',
    'depends' : ['hr', 'base',
                 'hr_attendance',
                 'hr_manual_attendance',
                 'gbs_hr_attendance_report',
                 'hr_rostering',
                 'base_technical_features',
                 'hr_overtime_requisition',
                 'yuko_report_layout',
                 'report_layout', 'resource',
                 'hr_attendance_and_ot_summary',],

    'data' : [
            'security/ir.model.access.csv',
            'views/hr_overtime_requisition_view.xml',
            'views/hr_attendance_view.xml',
            'views/hr_manual_attendance_view.xml',
            'reports/inherit_attendance_summary_report_template.xml',
            'reports/inherit_attendance_summr_report_view.xml',
            'reports/inherit_employee_attendance_report_template.xml',
            'reports/employee_work_schedule_report_view.xml',
            ],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
