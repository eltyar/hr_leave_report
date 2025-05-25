# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class HrLeaveProcessingTime(models.Model):
    _name = 'hr.leave.processing.time'
    _description = 'HR Leave Processing Time'
    
    leave_id = fields.Many2one('hr.holidays', string='Leave Request', required=True, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', string='Employee', related='leave_id.employee_id', store=True)
    department_id = fields.Many2one('hr.department', string='Department', related='leave_id.department_id', store=True)
    submission_date = fields.Datetime(string='Submission Date')
    manager_approval_date = fields.Datetime(string='Manager Approval Date')
    final_approval_date = fields.Datetime(string='Final Approval Date')
    processing_time = fields.Float(string='Processing Time (Hours)', compute='_compute_processing_time', store=True)
    processing_time_days = fields.Float(string='Processing Time (Days)', compute='_compute_processing_time', store=True)
    state = fields.Selection(related='leave_id.state', string='Status', store=True)
    
    @api.depends('submission_date', 'final_approval_date')
    def _compute_processing_time(self):
        for record in self:
            if record.submission_date and record.final_approval_date:
                # Calculate the time difference in hours
                diff = record.final_approval_date - record.submission_date
                hours = diff.total_seconds() / 3600
                record.processing_time = hours
                record.processing_time_days = hours / 24
            else:
                record.processing_time = 0
                record.processing_time_days = 0

class HrHolidays(models.Model):
    _inherit = 'hr.holidays'
    
    processing_time_ids = fields.One2many('hr.leave.processing.time', 'leave_id', string='Processing Time Records')
    
    @api.model
    def create(self, vals):
        res = super(HrHolidays, self).create(vals)
        # Create a processing time record when a leave request is created
        if res.type == 'remove':  # Only for leave requests, not allocations
            self.env['hr.leave.processing.time'].create({
                'leave_id': res.id,
                'submission_date': res.create_date,
            })
        return res
    
    def write(self, vals):
        result = super(HrHolidays, self).write(vals)
        # Update processing time records based on state changes
        if 'state' in vals:
            for record in self:
                processing_time = self.env['hr.leave.processing.time'].search([('leave_id', '=', record.id)], limit=1)
                if processing_time:
                    if vals['state'] == 'validate1' and not processing_time.manager_approval_date:
                        processing_time.write({'manager_approval_date': fields.Datetime.now()})
                    elif vals['state'] == 'validate' and not processing_time.final_approval_date:
                        processing_time.write({'final_approval_date': fields.Datetime.now()})
        return result
    
    # Create a cron job to calculate processing times from existing records
    @api.model
    def init_leave_processing_time(self):
        """
        Initialize processing time records for existing leave requests
        This method can be called manually or via a scheduled action
        """
        # Get all leave requests without processing time records
        leaves = self.search([('type', '=', 'remove'), ('processing_time_ids', '=', False)])
        
        for leave in leaves:
            # Create a basic processing time record
            proc_time = self.env['hr.leave.processing.time'].create({
                'leave_id': leave.id,
                'submission_date': leave.create_date,
            })
            
            # Try to find state change dates from mail tracking values
            message_ids = self.env['mail.message'].search([('model', '=', 'hr.holidays'), ('res_id', '=', leave.id)])
            
            for message in message_ids:
                tracking_values = self.env['mail.tracking.value'].search([('mail_message_id', '=', message.id), ('field', '=', 14717)])
                
                for tracking in tracking_values:
                    if tracking.new_value_char in ['confirm', 'Confirmed', 'إنتظار المدير المباشر']:
                        proc_time.write({'submission_date': message.date})
                    elif tracking.new_value_char in ['validate1', 'إنتظار الموارد البشرية']:
                        proc_time.write({'manager_approval_date': message.date})
                    elif tracking.new_value_char in ['validate', 'تم التصديق']:
                        proc_time.write({'final_approval_date': message.date})
