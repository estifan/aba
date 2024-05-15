import frappe
import requests
from requests.auth import HTTPDigestAuth
import json
from datetime import datetime, date, time, timedelta
from aba.biometric_attendance.device import hikvisionGetcheckIn

def addDailyCheckInToDoc():
    print("daily")
    employees = frappe.get_all('Employee', filters={'status': 'Active'}, fields=['name', "employee_name", 'attendance_device_id'])
    print(employees)
    frappe.delete_doc("Check In", "2024-05-15-Nebyou ame")
    a = frappe.get_all('Check In')
    print(a)
    for employee in employees:
        checkIn_Time = hikvisionGetcheckIn(employeeNo= employee['attendance_device_id'])
        print(checkIn_Time)
        try:
            frappe.get_doc("DocType", "Check In")
            print("Doctype already exists:", "Check In")
        except frappe.DoesNotExistError:
            print("Doctype already exists false:", "Check In")
            # newCheckIn = frappe.get_doc(
            #     {
            #         "doctype": "Check In",
            #         "employee_id": employee["name"],
            #         "employee_name": employee["employee_name"],
            #         "date": date.today(),
            #         "check_in_time": checkIn_Time,
            #         "status": "Normal",
            #     }
            # )
            # newCheckIn.insert()
            # frappe.db.commit()