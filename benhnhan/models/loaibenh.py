# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _


class LoaiBenh(models.Model):
    _name = 'qtsx.loaibenh'
    name = fields.Char('Tên loại', require=True)






