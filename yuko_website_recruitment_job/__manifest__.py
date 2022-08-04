
{
    'name' : 'Yuko Website',
    'version' : '1.0',
    'author' : 'Odoo Bangladesh',
    'summary': 'Website',
    'description': """
    
    """,
    'category': '',
    'sequence': 4,
    'website' : '',
    'depends' : ['web','hr_recruitment','website_hr_recruitment',],
    'data' : ['views/inherit_website_hr_recruitment_templates.xml',],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
