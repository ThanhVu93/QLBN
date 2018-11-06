# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import xlwt
import base64
from odoo import api, models, fields, _

class ReportFactoryOut(models.Model):
    _name = 'report.benhnhan.out'

    report_data = fields.Char('Name', size=256)
    file_name = fields.Binary('Excel Report', readonly=True)

class WizardValuationBenhNhan(models.Model):
    _name = 'qtsx.baocao'
    ngaykham = fields.Date('Ngày khám bệnh')

    @api.multi
    def baocao(self):
        self.ensure_one()
        report1 = self.env['qtsx.benhnhan'].search([])
        workbook = xlwt.Workbook()
        style15 = xlwt.easyxf('font: height 240, name Calibri; border: left thin, right thin, top thin, bottom thin')
        value = {}
        value['benhnhan'] = "Bệnh nhân"
        value['sodienthoai'] = "Số điện thoại"
        value['diachi'] = "Địa chỉ"
        new_sheet = workbook.add_sheet(value['benhnhan'].decode('utf-8'), cell_overwrite_ok=True)
        new_sheet.write(0, 0, value['benhnhan'].decode('utf-8'), style15)
        new_sheet.write(0, 1, value['sodienthoai'].decode('utf-8'), style15)
        new_sheet.write(0, 2, value['diachi'].decode('utf-8'), style15)
        row = 1
        for record in report1:
            value['benhnhan'] = record.name if record.name else ''
            value['sodienthoai'] = record.sodienthoai if record.sodienthoai else ''
            value['diachi'] = record.diachi if record.diachi else ''
            value['diaphuong'] = record.diaphuong if record.diaphuong else ''
            new_sheet.write(row, 0, value['benhnhan'], style15)
            new_sheet.write(row, 1, value['sodienthoai'], style15)
            new_sheet.write(row, 2, value['diachi'], style15)
            row = row + 1
        filename = ('Report' + '.xls')
        workbook.save(filename)
        fp = open(filename, "rb")
        file_data = fp.read()
        out = base64.encodestring(file_data)
        attach_vals = {
            'report_data': 'Report' + '.xls',
            'file_name': out,
        }
        act_id = self.env['report.benhnhan.out'].create(attach_vals)
        fp.close()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'report.benhnhan.out',
            'res_id': act_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'context': self.env.context,
            'target': 'new',
        }