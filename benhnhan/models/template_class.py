# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields
from odoo import api


class Many2One(models.Model):
    _name = 'many2one'
    name = fields.Char('Giá trị các trường liên kết', help='Bảng để liên kết many2one.')
    value = fields.Float()

class One2many(models.Model):
    _name = 'one2many'
    name = fields.Char('Giá trị các trường liên kết', help='Bảng để liên kết one2many')


class Many2Many(models.Model):
    _name = 'many2many'
    name = fields.Char('Liên kết nhiều nhiều', help='Liên kết nhiều nhiều')


class LessMinimalModel(models.Model):
    _name = 'test.model2'  # _name: Tên của models

    # string(unicode, default: field’s name)
    # required(bool, default: False)
    # help(unicode, default: ''): tooltip
    # index(bool, default: False)
    # digits(total, decimal): (Tổng số con số, số thập phân)
    # readonly

    # compute='hamtinhtoan': trường tính toán từ các trường khác
    # store = True : Các trường được tính toán (compute) không được lưu trữ theo mặc định.
    # store=True sẽ lưu trong cơ sở dữ liệu, có thể tìm kiếm
    # related : Lấy 1 trường của bảng khác lưu vào bảng hiện tại, thường phối hợp với store
    name = fields.Char('Tên', required=True, help='Tooltip')
    bool = fields.Boolean(help='Đúng/Sai')
    interger = fields.Integer(help='Kiếu số nguyên')
    float = fields.Float(help='Kiểu số thực', digits=(16, 2))
    text = fields.Text(help='Văn bản ngắn')
    selection = fields.Selection([
        ('1', 'Lựa chọn 1'),
        ('2', 'Lựa chọn 2')
    ], help='Lựa chọn')
    note = fields.Html('Note', help='Kiểu texteditor')
    date = fields.Date(help='Kiểu ngày, có các hàm liên quan')
    datetime = fields.Datetime(help='Kiểu ngày, có các hàm liên quan')
    many2one = fields.Many2one('many2one', domain=[('name', '!=', '1'), ('name', '!=', '123')],
                               help='Bảng liên kết n<->1, nhiều dòng ở bảng này có thể liên kết dòng ở bảng many2one')
    one2many = fields.One2many('one2many', 'id',
                               help='Liên kết 1<->n, 1 dòng ở  bảng này được liên kết bởi nhiều dòng của bảng model2')
    many2many = fields.Many2many('many2many', 'id', 'id', help='Liên kết nhiều nhiều')

    value = fields.Float()
    tax = fields.Float()
    total = fields.Float(compute='_compute_total')
    many2onename = fields.Char(related='many2one.name', store=True)

# region Trường tính toán(compute) dùng depends
@api.depends('value') # Các trường sử dụng
def _compute_total(self):
    for record in self:
        if record.value:
            record.total = record.value + record.value


@api.depends('many2one.value') # Trường sử dụng nằm ở bảng con
def _compute_total_sub(self):
    for record in self:
        record.total = sum(line.value for line in record.many2one)
# endregion


# region sự kiện onchange
# Sự kiện áp dụng khi dữ liệu chưa lưu vào databse, làm thay đổi các trường khác, thay đổi cách hiển thị...
# Có thể bật tắt trong file giao diện <field name="note" on_change="0"/>, 0: tắt;
@api.onchange('name', 'text') # Nếu field name hoặc field text thay đổi sẽ gọi hàm này
def check_change(self):
    if self.name == '100' & self.text == '43423':
        self.note = True
# endregion


# region class Kế thừa
class Inheritance0(models.Model):
    _name = 'inheritance.0'
    _description = 'Inheritance Zero'

    name = fields.Char()

    def call(self):
        return self.check("model 0")

    def check(self, s):
        return "This is {} record {}".format(s, self.name)


class Inheritance1(models.Model):
    _name = 'inheritance.1'
    _inherit = 'inheritance.0'
    _description = 'Inheritance One'

    def call(self):
        return self.check("model 1")


# endregion


# region class Mở rộng
class Extension0(models.Model):
    _name = 'extension.0'
    _description = 'Extension zero'
    name = fields.Char(default="A")


class Extension1(models.Model):
    _inherit = 'extension.0'
    description = fields.Char(default="Extended")


# endregion


# region Phương thức/ Hàm bình thường
def a_method(self):
    self.do_operation()


def do_operation(self):
    print self  # => a.model(1, 2, 3, 4, 5)
    for record in self:
        print record  # => a.model(1), then a.model(2), then a.model(3), ...


# endregion


# region Lọc dữ liệu
def LocDuLieu(self):
    for record in self:
        record.filtered(lambda r: r.name != "Không rỗng")
# endregion


# region Sắp xếp dữ liệu
def SapXep(self):
    for record in self:
        record.sorted(key=lambda r: r.name)
# endregion


# region Search/Tìm dữ liệu
def Search(self):
    records = self.search([('name', '!=', "Không rỗng"), ('name', '!=', "")])
# endregion


