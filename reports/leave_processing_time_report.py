# -*- coding: utf-8 -*-
from odoo import models, fields, tools, api

class LeaveProcessingTimeReport(models.Model):
    _name = 'leave.processing.time.report'
    _description = 'Leave Processing Time Analysis Report'
    _auto = False
    
    leave_id = fields.Many2one('hr.holidays', string='Leave Request', readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', readonly=True)
    department_id = fields.Many2one('hr.department', string='Department', readonly=True)
    submission_date = fields.Datetime(string='Submission Date', readonly=True)
    manager_approval_date = fields.Datetime(string='Manager Approval Date', readonly=True)
    final_approval_date = fields.Datetime(string='Final Approval Date', readonly=True)
    processing_time = fields.Float(string='Processing Time (Hours)', readonly=True)
    processing_time_days = fields.Float(string='Processing Time (Days)', readonly=True)
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('confirm', 'To Approve'),
        ('refuse', 'Refused'),
        ('validate1', 'Second Approval'),
        ('validate', 'Approved'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True)
    
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    pt.id AS id,
                    pt.leave_id AS leave_id,
                    pt.employee_id AS employee_id,
                    pt.department_id AS department_id,
                    pt.submission_date AS submission_date,
                    pt.manager_approval_date AS manager_approval_date,
                    pt.final_approval_date AS final_approval_date,
                    pt.processing_time AS processing_time,
                    pt.processing_time_days AS processing_time_days,
                    hl.state AS state
                FROM
                    hr_leave_processing_time pt
                JOIN
                    hr_holidays hl ON pt.leave_id = hl.id
                WHERE
                    hl.type = 'remove'
            )
        """ % (self._table))
