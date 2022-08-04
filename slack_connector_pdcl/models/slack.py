# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, SUPERUSER_ID


class Company(models.Model):
    _inherit = 'res.company'

    att_monitor_channel_id = fields.Many2one('slack.channel', string="Attendance Monitor Channel")


class DeviceDetail(models.Model):
    _inherit = 'hr.attendance.device.detail'

    @api.model
    def pull_automation(self):
        super(DeviceDetail, self).pull_automation()
        self.att_monitoring_msg_for_slack()

    @api.model
    def att_monitoring_msg_for_slack(self):
        data = {}
        emp_pool = self.env['hr.employee']
        att_utility_pool = self.env['attendance.utility']
        curr_time_gmt = fields.datetime.now()
        current_time = curr_time_gmt + timedelta(hours=6)
        requested_date = data['required_date'] = curr_time_gmt.strftime("%Y-%m-%d")
        graceTime = att_utility_pool.getGraceTime(requested_date)
        for rec in self.search([]):
            msg = self._prepare_att_monitoring_message(rec.operating_unit_id, data, graceTime, emp_pool, att_utility_pool, current_time)
            if msg and self.env.user.company_id.att_monitor_channel_id:
                self.env.user.company_id.att_monitor_channel_id.post_message_webhook(msg)

    @api.model
    def _prepare_att_monitoring_message(self, operating_unit, data, graceTime, emp_pool, att_utility_pool, current_time):
        pool = self.env['report.gbs_hr_attendance_report.report_daily_att_doc']
        att_summary = pool.getSummaryByUnit(operating_unit, data, graceTime,  emp_pool, att_utility_pool, current_time)
        if not att_summary.get('late', False) and not att_summary.get('absent', False):
            return False

        msg = ""
        # msg += "*** TESTING ***\r\n"
        # msg += "\r\n==============================================="
        msg += "*Attendance Report*\r\n"
        msg += "\r\n*Late Employee*\r\n"
        # msg += str(len(att_summary.get('late', False))) if att_summary.get('late', False) else str(0)
        if att_summary.get('late', False):
            msg += "```"
            for lemp in att_summary.get('late', False):
                msg += str(lemp.name).ljust(30) + " >>  " + lemp.check_in.strftime("%H:%M %p") + "\r\n"
            msg += "```"

        msg += "\r\n*Absent Employee*\r\n"
        # msg += str(len(att_summary.get('absent', False))) if att_summary.get('absent', False) else str(0)
        if att_summary.get('absent', False):
            msg += "```"
            for abs in att_summary.get('absent', False):
                msg += str(abs.name) + "\r\n"
            msg += "```"

        return msg
