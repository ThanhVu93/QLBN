# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _


class KhamBenh(models.Model):
    _name = 'qtsx.khambenh'
    chuandoan = fields.Char('Chuẩn đoán', require=True)
    ngaykhambenh = fields.Datetime('Ngày/Giờ khám bệnh', require=True)
    benhnhan = fields.Many2one('qtsx.benhnhan', 'name')
    loaibenh = fields.Many2one('qtsx.loaibenh', 'name')
    ghichu = fields.Text('Ghi chú')





