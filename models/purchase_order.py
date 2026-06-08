from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    partner_id = fields.Many2one(domain="[('contact_type', '=', 'vendor')]")
    vendor_id = fields.Char(
        string='Vendor ID',
        related='partner_id.vendor_id',
        readonly=True,
    )
