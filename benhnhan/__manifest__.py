# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Benh Nhan',
    'version': '1.0',
    'sequence': 121,
    'depends': ['web'],
    'author': 'Thanh Vu',
    'category': 'Benh Nhan',
    'website': 'http://liink.vn/',
    'data': [
        'views/web_custom.xml',
        'views/web_custom_templates.xml',
        'views/benhnhan_views.xml',
        'views/diaphuong_views.xml',
        'views/loaibenh_views.xml',
        'views/khambenh_views.xml',
        'wizard/wizard_valuation_benhnhan.xml',
        'views/template_class.xml',
        'views/benhnhan_menu.xml',
    ],
    'qweb': [
        'static/src/xml/web_t_name_custom.xml',
        'static/src/xml/webkanban_t_name_custom.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
