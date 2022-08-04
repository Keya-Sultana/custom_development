from openerp import models, fields,_
from openerp import api
from odoo.http import request
import pyodbc
import datetime
from datetime import timedelta
import logging
_logger = logging.getLogger(__name__)

from odoo.exceptions import Warning, ValidationError
from openerp import http


driver = '{ODBC Driver 13 for SQL Server}'
IN_CODE = 'IN'
OUT_CODE = 'OUT'
RFID_IN_CODE = 'IN_RFID'
VALID_DATA = "Valid"

MAX_ATTEMPT_TO_SUCCESS = 5

get_BADGENUMBER = """SELECT DISTINCT (usr.BADGENUMBER)
                     FROM CHECKINOUT att
                     JOIN USERINFO usr ON usr.USERID = att.USERID
                     WHERE att.IsRead = 0 AND att.Id <= ?"""

get_employee_ids = """SELECT device_employee_acc, id
                      FROM hr_employee WHERE device_employee_acc IN %s"""

get_att_data_sql = """SELECT
                          usr.BADGENUMBER, att.VERIFYCODE, att.CHECKTIME, att.SENSORID
                      FROM CHECKINOUT att
                      JOIN USERINFO usr ON usr.USERID = att.USERID
                      WHERE att.IsRead = 0 AND att.Id <= ?
                      ORDER BY usr.BADGENUMBER, att.CHECKTIME ASC"""


class DeviceDetail(models.Model):
    _inherit = 'hr.attendance.device.detail'


    def isValidByDuration(self, currentRow, previousRow, deviceInOutCode, tolerableSecond):

        # usr.BADGENUMBER, att.VERIFYCODE, att.CHECKTIME, att.SENSORID

        if len(previousRow) == 0:
            return True

        # Check same Employee or not
        if currentRow[0] != previousRow[0]:
            return True

        currentType = ""
        previousType = ""

        # Get same attendance type or not

        if (deviceInOutCode.get(str(currentRow[3])) == IN_CODE or deviceInOutCode.get(str(currentRow[3])) == RFID_IN_CODE):
            currentType = IN_CODE
        elif deviceInOutCode.get(str(currentRow[3])) == OUT_CODE:
            currentType = OUT_CODE

        if (deviceInOutCode.get(str(previousRow[3])) == IN_CODE or deviceInOutCode.get(str(previousRow[3])) == RFID_IN_CODE):
            previousType = IN_CODE
        elif deviceInOutCode.get(str(previousRow[3])) == OUT_CODE:
            previousType = OUT_CODE

        # Check same attendance type or not
        if currentType != previousType:
            return True

        # Check tolerable duration
        durationInSecond = (currentRow[2] - previousRow[2]).total_seconds()
        if durationInSecond > tolerableSecond:
            return True
        else:
            return False


    def storeData(self, row, deviceInOutCode, employeeIdMap, operatingUnitId):

        hr_att_pool = self.env['hr.attendance']

        employeeId = employeeIdMap.get(row[0])

        if(deviceInOutCode.get(str(row[3])) == IN_CODE or deviceInOutCode.get(str(row[3])) == RFID_IN_CODE):
            self.createData(row, employeeId, IN_CODE, hr_att_pool, operatingUnitId)
        elif(deviceInOutCode.get(str(row[3])) == OUT_CODE):

            preAttData = hr_att_pool.search([('employee_id', '=', employeeId),
                                             ('check_in', '!=',False)], limit=1, order='check_in desc')

            # preAttData = hr_att_pool.search([('employee_id', '=', employeeId)], limit=1,
            #                                                   order='check_in desc')

            if preAttData and preAttData.check_out is False:
                chk_in = self.getDateTimeFromStr(preAttData.check_in)
                durationInHour = (self.convertDateTime(row[2]) - chk_in).total_seconds() / 60 / 60
                if durationInHour <=15 and durationInHour >= 0:
                    preAttData.write({'check_out': self.convertDateTime(row[2]),
                                      'worked_hours':durationInHour,
                                      'write_date':datetime.datetime.now(),
                                      'has_error': False,
                                      'operating_unit_id': operatingUnitId
                                      })
                else:
                    self.createData(row, employeeId, OUT_CODE, hr_att_pool, operatingUnitId)
            else:
                self.createData(row, employeeId, OUT_CODE, hr_att_pool, operatingUnitId)


    def saveAsError(self, row, employeeIdMap, deviceInOutCode, operatingUnitId, reason):

        attendance_error_obj = self.env['hr.attendance.import.error']

        error_vals = {}
        if (deviceInOutCode.get(str(row[3])) == IN_CODE or deviceInOutCode.get(str(row[3])) == RFID_IN_CODE):
            error_vals['check_in'] = self.convertDateTime(row[2])
        else:
            error_vals['check_out'] = self.convertDateTime(row[2])

        if employeeIdMap.get(row[0]) is not None:
            error_vals['employee_id'] = employeeIdMap.get(row[0])
        else:
            error_vals['employee_code'] = row[0]

        error_vals['operating_unit_id'] = operatingUnitId
        error_vals['reason'] = reason

        attendance_error_obj.create(error_vals)

    def isValidData(self, row, deviceInOutCode, employeeIdMap):

        if row[0] is None: # Check device_employee_acc is not null
            return "Empty Acc No"
        if employeeIdMap.get(row[0]) is None: # Check device_employee_acc is mapped or not
            return  "Unmapped Emp Acc"
        if row[1] is None: # Check in_out code is not null
            return "Empty Code"
        if deviceInOutCode.get(str(row[3])) != IN_CODE and deviceInOutCode.get(str(row[3])) != RFID_IN_CODE and deviceInOutCode.get(str(row[3])) != OUT_CODE: # Check in_out code is valid or not
            return "Unmapped Code"
        if row[2] is None: # Check time is not null
            return "Empty Check Time"
        if row[3] is None: # Check sensor_id is not null
            return "Empty Sensor ID"
        return VALID_DATA
