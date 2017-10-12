# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import fields, models
from openerp.tools.translate import _


class Company(models.Model):
    _inherit = 'res.company'

    product_rejected_limit_hours = fields.Float(
        string=u'Limit of hours to record negations of products',
        default=24,
        help="Not registering when the same product is detected for the same customer/supplier as a product denied within this time limit.")
