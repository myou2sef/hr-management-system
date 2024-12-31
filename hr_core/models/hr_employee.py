from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date

class HrEmployee(models.Model):
    _name = 'hr.employee'
    _description = 'Employee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    # Basic Information
    name = fields.Char(string='Name', required=True, tracking=True)
    employee_id = fields.Char(string='Employee ID', required=True, copy=False, 
                            readonly=True, default=lambda self: _('New'))
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    
    # Personal Information
    first_name = fields.Char(string='First Name', required=True, tracking=True)
    last_name = fields.Char(string='Last Name', required=True, tracking=True)
    arabic_name = fields.Char(string='Arabic Name')
    birth_date = fields.Date(string='Date of Birth', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], required=True, tracking=True)
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed')
    ], string='Marital Status', tracking=True)
    
    # Contact Information
    work_email = fields.Char(string='Work Email')
    personal_email = fields.Char(string='Personal Email')
    work_phone = fields.Char(string='Work Phone')
    mobile_phone = fields.Char(string='Mobile Phone')
    emergency_contact = fields.Char(string='Emergency Contact')
    emergency_phone = fields.Char(string='Emergency Phone')
    
    # Job Information
    department_id = fields.Many2one('hr.department', string='Department', tracking=True)
    position_id = fields.Many2one('hr.position', string='Position', tracking=True)
    parent_id = fields.Many2one('hr.employee', string='Manager')
    child_ids = fields.One2many('hr.employee', 'parent_id', string='Subordinates')
    coach_id = fields.Many2one('hr.employee', string='Coach')
    job_grade = fields.Char(string='Job Grade')
    
    # Employment Information
    joining_date = fields.Date(string='Joining Date', tracking=True)
    contract_end_date = fields.Date(string='Contract End Date')
    work_location = fields.Char(string='Work Location')
    work_schedule = fields.Selection([
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contractor', 'Contractor')
    ], string='Work Schedule', default='full_time')
    
    # Documents and Identification
    identification_id = fields.Char(string='Identification No', tracking=True)
    passport_id = fields.Char(string='Passport No')
    bank_account_id = fields.Many2one('res.partner.bank', string='Bank Account')
    
    # System Fields
    color = fields.Integer(string='Color Index')
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('approved', 'Approved'),
        ('refused', 'Refused')
    ], string='Status', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('employee_id', _('New')) == _('New'):
            vals['employee_id'] = self.env['ir.sequence'].next_by_code('hr.employee') or _('New')
        result = super(HrEmployee, self).create(vals)
        return result

    @api.constrains('identification_id')
    def _check_identification_id(self):
        for record in self:
            if record.identification_id:
                employee = self.search([
                    ('identification_id', '=', record.identification_id),
                    ('id', '!=', record.id)
                ])
                if employee:
                    raise ValidationError(_('Identification No must be unique!'))

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for employee in self:
            employee.name = f"{employee.first_name} {employee.last_name}"

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_refuse(self):
        self.write({'state': 'refused'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})

    @api.constrains('birth_date')
    def _check_birth_date(self):
        for record in self:
            if record.birth_date and record.birth_date > date.today():
                raise ValidationError(_('Birth date cannot be in the future!'))

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.employee_id}] {record.name}"
            result.append((record.id, name))
        return result
