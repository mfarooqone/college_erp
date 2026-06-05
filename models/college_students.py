from odoo import api, models, fields


class CollegeStudents(models.Model):
    _name = 'college.students'
    _description = 'College student details'

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

    @api.onchange('same_as_communication', 'communication_address')
    def _onchange_same_as_communication(self):
        if self.same_as_communication:
            self.permanent_address = self.communication_address

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
