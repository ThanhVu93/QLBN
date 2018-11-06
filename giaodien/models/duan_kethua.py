# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _

class project_task_inherit(models.Model):
    _inherit = 'project.task'
    ngaybatdau = fields.Datetime('Ngày bắt đầu', index=True)
    ngayketthuc = fields.Datetime('Ngày kết thúc', index=True)
    ThoiGianUocLuong = fields.Integer('Thời gian ước lượng', index=True)
    ThoiGianThucTe = fields.Integer('Thời gian thực tế', index=True)
    progress = fields.Selection([('0', '0%'), ('1', '10%'), ('2', '20%'), ('3', '30%'),
    ('4', '49%'), ('5', '50%'),('6', '60%'), ('7', '70%'), ('8', '80%'),('9', '90%'),('10', '100%')
                                 ], 'Tiến độ', default='0')
    UuTien = fields.Selection([('0', 'Thấp'), ('1', 'Trung bình'), ('2', 'Cao'), ('3', 'Rất cao')
                                 ], 'Ưu tiên', default='1')
    project_task_ids = fields.Many2many('res.users', 'project_user_rel', 'uid', 'task_id', string='Phân công cho')






