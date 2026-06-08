from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_id = fields.Many2one(domain="[('contact_type', '=', 'customer')]")
    customer_id = fields.Char(
        string='Customer ID',
        related='partner_id.customer_id',
        readonly=True,
    )
