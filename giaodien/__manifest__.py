# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Giao dien',
    'version': '1.0',
    'sequence': 121,
    'depends': ['web', 'project'],
    'author': 'By Liink Company',
    'category': 'Manufacturing',
    'website': 'http://liink.vn/',
    'data': [
        'views/web_custom.xml',
        'views/web_custom_templates.xml',
        'views/duan_kethua_views.xml',
        'views/loai_views.xml',
    ],
    'qweb': [
        'static/src/xml/web_t_name_custom.xml',
        'static/src/xml/webkanban_t_name_custom.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
