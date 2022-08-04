# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name' : 'YUKO Employee IOU',
    'version' : '10.0.1.0.0',
    'author' : 'Odoo Bangladesh',
    'summary': 'HR Employee IOU',
    'description': """
    
    """,
    'category': 'employee',
    'sequence': 4,
    'website' : '',
    'depends' : ['base',
                'hr', 'mail',
                'hr_employee_iou',
                'gbs_application_group',
                'gbs_hr_security',
                 ],

    'data' : [
            "security/security.xml",
            "security/ir.model.access.csv",
            "views/hr_employee_iou_view.xml",
    ],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
