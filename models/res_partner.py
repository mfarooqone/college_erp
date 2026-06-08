from odoo import api, fields, models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'college.erp.contact.id.mixin']

    _customer_id_unique = models.Constraint('UNIQUE (customer_id)', 'Customer ID must be unique.')
    _vendor_id_unique = models.Constraint('UNIQUE (vendor_id)', 'Vendor ID must be unique.')
    _employee_id_unique = models.Constraint('UNIQUE (employee_id)', 'Employee ID must be unique.')

    contact_type = fields.Selection([
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('employee', 'Employee'),
    ], string='Contact Type', required=True)

    customer_id = fields.Char(string='Customer ID', readonly=True, copy=False)
    vendor_id = fields.Char(string='Vendor ID', readonly=True, copy=False)
    employee_id = fields.Char(string='Employee ID', readonly=True, copy=False)
    contact_code = fields.Char(string='ID', compute='_compute_contact_code')
    is_internal_company = fields.Boolean(string='Internal Company', readonly=True)

    @api.model
    def _company_partner_ids(self):
        return set(self.env['res.company'].sudo().search([]).mapped('partner_id').ids)

    @api.depends('contact_type', 'customer_id', 'vendor_id', 'employee_id')
    def _compute_contact_code(self):
        for partner in self:
            field = self._contact_id_field(partner.contact_type)
            partner.contact_code = partner[field] if field else False

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        if 'contact_type' not in fields_list:
            return values
        mode = self.env.context.get('res_partner_search_mode')
        if mode == 'customer':
            values['contact_type'] = 'customer'
        elif mode == 'supplier':
            values['contact_type'] = 'vendor'
        elif self.env.context.get('default_contact_type') == 'employee':
            values['contact_type'] = 'employee'
        return values

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        internal_ids = self._company_partner_ids()
        for partner in partners:
            if partner.id in internal_ids:
                partner.write({
                    'is_internal_company': True,
                    'customer_id': False,
                    'vendor_id': False,
                    'employee_id': False,
                })
                continue
            field = self._contact_id_field(partner.contact_type)
            if field and not partner[field]:
                partner[field] = self._next_contact_id(partner.contact_type)
        return partners

    @api.model
    def _sync_all_contact_sequences(self):
        """Called on module upgrade — fix internal company partner, backfill IDs, sync counters."""
        self.with_context(active_test=False).search([
            ('contact_type', '=', 'company'),
        ]).write({'contact_type': 'customer'})

        internal_ids = self.env['res.company'].sudo().search([]).mapped('partner_id').ids
        skip_ids = internal_ids or [0]
        if internal_ids:
            self.browse(internal_ids).write({
                'is_internal_company': True,
                'customer_id': False,
                'vendor_id': False,
                'employee_id': False,
            })
        self.search([
            ('is_internal_company', '=', True),
            ('id', 'not in', skip_ids),
        ]).write({'is_internal_company': False})

        for contact_type, field_name in (
            ('customer', 'customer_id'),
            ('vendor', 'vendor_id'),
            ('employee', 'employee_id'),
        ):
            missing = self.search([
                ('contact_type', '=', contact_type),
                ('id', 'not in', skip_ids),
                '|', (field_name, '=', False), (field_name, '=', ''),
            ])
            for partner in missing:
                partner[field_name] = self._next_contact_id(contact_type)

        return super()._sync_all_contact_sequences()
