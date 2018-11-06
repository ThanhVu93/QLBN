# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _


class BenhNhan(models.Model):
    _name = 'qtsx.benhnhan'
    name = fields.Char('Tên', require=True)
    sodienthoai = fields.Char('Số điện thoại', require=True)
    diachi = fields.Char('Địa chỉ', require=True)
    diaphuong = fields.Many2one('qtsx.diaphuong', 'name')







