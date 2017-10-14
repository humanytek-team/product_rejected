# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from datetime import datetime

from openerp import api, fields, models
from openerp.exceptions import ValidationError
from openerp.tools.translate import _


class ProductRejected(models.Model):
    """record the number of times a product for any reason cannot be
    sold/purchased from a customer/supplier."""

    _name = 'product.rejected'

    product_tmpl_id = fields.Many2one(
        'product.template', 'Product', required=True)
    product_id = fields.Many2one(
        'product.product',
        'Product (variant)',
        required=True)
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

    @api.constrains('date')
    def _check_date(self):
        """Check limit of time to record product negations to same partner"""

        limit_hours = self.env.user.company_id.product_rejected_limit_hours
        if limit_hours > 0:

            for record in self:

                if record.partner_id:
                    last_record = self.search([
                        ('id', '!=', record.id),
                        ('product_id', '=', record.product_id.id),
                        ('partner_id', '=', record.partner_id.id),
                        ('company_id', '=', self.env.user.company_id.id),
                        ], order='date')

                    if last_record:
                        last_record_date = last_record[-1].date
                        last_record_datetime = datetime.strptime(
                            last_record_date, '%Y-%m-%d %H:%M:%S')
                        record_date = datetime.strptime(
                            record.date, '%Y-%m-%d %H:%M:%S')

                        diff = record_date - last_record_datetime
                        hours_diff = (diff.seconds / 60.0) / 60

                        if hours_diff <= limit_hours:
                            raise ValidationError(
                                _('This product rejected has already been registered for this same partner in the last %s hours.' % limit_hours)
                                )

class ProductTemplate(models.Model):
    """Inheritance of model product.template base"""

    _inherit = 'product.template'

    products_rejected_ids = fields.One2many(
        'product.rejected',
        'product_tmpl_id',
        'Product negations')

    count_product_negations = fields.Integer(
        'Counter of product negations',
        compute='_compute_count_product_negations')

    @api.depends('products_rejected_ids')
    def _compute_count_product_negations(self):
        """Computes value of field count_product_negations"""

        for record in self:
            record.count_product_negations = len(record.products_rejected_ids)
