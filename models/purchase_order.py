from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # Only vendors appear in the Vendor field on RFQs/orders.
    partner_id = fields.Many2one(domain="[('contact_type', '=', 'vendor')]")

    # Related field for list/kanban views (e.g. VEND/00001 next to vendor name).
    vendor_id = fields.Char(
        string='Vendor ID',
        related='partner_id.vendor_id',
        readonly=True,
    )
