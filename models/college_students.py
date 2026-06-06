from odoo import api, models, fields


class CollegeStudents(models.Model):
    _name = 'college.students'
    _description = 'College student details'

    PROGRAM_SELECTION = [
        ('computer_science', 'Computer Science'),
        ('information_technology', 'Information Technology'),
        ('software_engineering', 'Software Engineering'),
        ('business_administration', 'Business Administration'),
        ('electrical_engineering', 'Electrical Engineering'),
    ]

    SEMESTER_SELECTION = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
    ]

    GUARDIAN_RELATION_SELECTION= [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
        ('other', 'Other'),
    ]

    partner_id = fields.Many2one(
        'res.partner',
        string='Contact',
        ondelete='restrict',
        domain="[('is_company', '=', False)]",
    )
    image_1920 = fields.Image(string='Photo', max_width=1920, max_height=1920)
    image_128 = fields.Image(string='Photo (128)', related='image_1920', max_width=128, max_height=128, store=True)
    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection(string='Gender', selection=[('male', 'Male'), ('female', 'Female')])
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    communication_address = fields.Text(string='Communication Address')
    permanent_address = fields.Text(string='Permanent Address')
    same_as_communication = fields.Boolean(
        string='same as communication address',
        default=True,
    )
    admission_number = fields.Char(string='Admission Number', required=True)
    admission_date = fields.Date(string='Admission Date', required=True)
    program = fields.Selection(
        string='Program',
        selection=PROGRAM_SELECTION,
    )
    batch = fields.Char(string='Batch')
    semester = fields.Selection(
        string='Semester',
        selection=SEMESTER_SELECTION,
    )
    guardian_name = fields.Char(string='Guardian Name')
    guardian_relation = fields.Selection(
        string='Relation',
        selection=GUARDIAN_RELATION_SELECTION,
    )
    guardian_phone = fields.Char(string='Guardian Phone')
    guardian_email = fields.Char(string='Guardian Email')
    notes = fields.Text(string='Internal Notes')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if not self.partner_id:
            return
        partner = self.partner_id
        self.name = partner.name
        self.email = partner.email
        self.phone = partner.phone or partner.mobile
        if partner.image_1920:
            self.image_1920 = partner.image_1920
        address_parts = [
            part for part in (
                partner.street,
                partner.street2,
                partner.city,
                partner.state_id.name if partner.state_id else False,
                partner.zip,
                partner.country_id.name if partner.country_id else False,
            ) if part
        ]
        if address_parts:
            self.communication_address = ', '.join(address_parts)
            if self.same_as_communication:
                self.permanent_address = self.communication_address

    @api.onchange('same_as_communication', 'communication_address')
    def _onchange_same_as_communication(self):
        if self.same_as_communication:
            self.permanent_address = self.communication_address

    def action_open_partner(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Contact',
            'res_model': 'res.partner',
            'res_id': self.partner_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('same_as_communication'):
                vals['permanent_address'] = vals.get('communication_address')
        return super().create(vals_list)

    def write(self, vals):
        res = super().write(vals)
        for student in self.filtered('same_as_communication'):
            if student.permanent_address != student.communication_address:
                super(CollegeStudents, student).write({
                    'permanent_address': student.communication_address,
                })
        return res
