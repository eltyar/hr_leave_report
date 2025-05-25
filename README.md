# HR Leave Processing Time Report

This module adds functionality to track and analyze the processing time of leave requests in Odoo.

## Features

- Track the processing time from submission to final approval
- Analyze average processing times by department, employee, or leave type
- Dashboard view for HR managers to monitor processing efficiency
- Reports to identify bottlenecks in the approval process

## Installation

1. Clone this repository to your Odoo addons directory
2. Update your Odoo apps list
3. Install the module through the Odoo UI

## Usage

After installation, the module will automatically start tracking processing time for new leave requests.
For existing leave requests, a scheduled action is provided to retroactively calculate processing times.

## Reports

The module adds the following reports:
- Leave Processing Time Analysis
- Average Processing Time by Department

## Dependencies

- hr_holidays module
