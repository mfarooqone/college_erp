from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    contact_type = fields.Selection([
        ('contact', 'Contact'),
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('employee', 'Employee'),
        ('company', 'Company'),
    ], string='Contact Type', default='contact')
