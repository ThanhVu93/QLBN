# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _


class Loai(models.Model):
    _name = 'qtsx.loai'

    name = fields.Char('Name', require=True)
class project_task(models.Model):
    _inherit = 'project.task'
    loai = fields.Many2one('qtsx.loai', 'name')








