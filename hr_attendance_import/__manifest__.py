{
    'name': 'HR Attendance Import',
    'author':  'Odoo Bangladesh',
    'website': 'www.odoo.com.bd',
    'license': 'LGPL-3',
    'version': "15.0.1.0.0",
    'category': 'HR Attendance',
    'data': [       
       'security/security.xml',
       'security/ir.model.access.csv',
       # 'views/hr_attendance_import_view.xml',
       # 'wizards/hr_attendance_import_wizard_view.xml',
    ],
    
    'depends': [
        'hr_attendance', 
        'hr', 
        'hr_holidays', 
       
    ],    
    
    'description': """This module enables HR Manager to import attendance data""",        
  
    'installable': True,
    'application': True,
}