# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from datetime import datetime

from openerp import fields, models


class ProductRejected(models.Model):
    """record the number of times a product for any reason cannot be
    sold/purchased from a customer/supplier."""

    _name = 'product.rejected'

    product_tmpl_id = fields.Many2one(
        'product.template', 'Product', required=True)
    product_id = fields.Many2one(
        'product.product', 'Product (variant)', required=True)
    partner_id = fields.Many2one('res.partner', 'Partner')
    date = fields.Datetime(
        'Date',
        required=True,
        default=lambda self: datetime.now())
    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True,
        default=lambda self: self.env.user.company_id.id,
        readonly=True)
    qty = fields.Integer('Quantity', default=1)


class ProductTemplate(models.Model):
    """Inheritance of model product.template base"""

    _inherit = 'product.template'

    products_rejected_ids = fields.One2many(
        'product.rejected',
        'product_tmpl_id',
        'Product negations')
