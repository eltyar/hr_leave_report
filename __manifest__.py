# -*- coding: utf-8 -*-
{
    'name': 'HR Leave Processing Time',
    'version': '1.0',
    'summary': 'Track and analyze processing time for leave requests',
    'description': """
        This module adds reports and dashboard elements to track the average processing time
        of leave requests from submission to final approval.
    """,
    'category': 'Human Resources',
    'author': 'El Tayar',
    'website': 'https://www.example.com',
    'depends': ['hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_leave_processing_time_views.xml',
        'reports/leave_processing_time_report.xml',
    ],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}