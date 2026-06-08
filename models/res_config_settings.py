from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    use_custom_invoice = fields.Boolean(
        string='Active invoice customization',
        config_parameter='college_erp.use_custom_invoice',
    )