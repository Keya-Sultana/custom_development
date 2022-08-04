
{
    'name' : 'Yuko Leaves',
    'version' : '1.0',
    'author' : 'Odoo Bangladesh',
    'summary': 'Leaves',
    'description': """
    Leaves Request for Employee
    """,
    'category': 'Human Resources',
    'sequence': 4,
    'website' : '',
    'depends' : ['hr_holidays',
                 'hr_holiday_utility',
                 'hr_short_leave',
                 'gbs_hr_public_holidays',
                 'gbs_application_group',
                 'hr_holidays_multi_levels_approval',],
    'data' : ["views/inherit_hr_holidays_views.xml",
              "views/inherit_hr_holidays_status_views.xml",
              "views/inherit_hr_holiday_import_view.xml",
              "views/hr_short_leave_views.xml",
              "views/earn_leave_menu.xml",],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
