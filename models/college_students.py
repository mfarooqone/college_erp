from odoo import models, fields

class CollegeStudents(models.Model):
    _name = 'college.students'
    _description = 'College student details'

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection(string='Gender', selection=[('male', 'Male'), ('female', 'Female')])
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    admission_number = fields.Char(string='Admission Number', required=True)
    admission_date = fields.Date(string='Admission Date', required=True)
