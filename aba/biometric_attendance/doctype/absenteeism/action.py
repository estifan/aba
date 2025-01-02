from aba.biometric_attendance.doctype.lateness.calculateLateness import calculateEarlyOut, exc_date
import frappe
import requests
from requests.auth import HTTPDigestAuth
import json
import frappe.share
from datetime import datetime, date, time, timedelta
from aba.biometric_attendance.device import hikvisionGetAbsenteeism
from frappe.desk.form.assign_to import add

def addDailyAbsenteeismToDoc(): 
    employees = frappe.get_all('Employee', filters={'status': 'Active'}, fields=['name', "employee_name","user_id", 'attendance_device_id','shift_type','reports_to'])
    for employee in employees:
        print(employee['attendance_device_id'])
        print("shift_type: ",employee['shift_type'])
        if  employee['shift_type']:
            shift = frappe.get_doc('ABAshift', employee['shift_type']).as_dict()
            if len(shift.list_of_days):
                filtered_arr = [d for d in shift.list_of_days if exc_date(d.day_of_the_week)-1 == date.today().weekday()]
                if len(filtered_arr):
                    print("day_of_the_week: ",filtered_arr[0].day_of_the_week)
                    continue
            # check if employee is on leave
            leave = frappe.get_all('Attendance', filters={"status":"On Leave",'attendance_date': date.today(),"employee": employee['name']}, fields=['name'])
            print("leave", leave)
            if len(leave):
                continue
            print("not on leave")
            Absenteeism = hikvisionGetAbsenteeism(employeeNo= employee['attendance_device_id'],device=shift["device"])
            manager = {}
            if(employee["reports_to"]): 
                manager = frappe.get_all('Employee', filters={'status': 'Active','name':  employee["reports_to"]}, fields=["user_id"])[0]
            print(Absenteeism)
            if(Absenteeism):
                try:
                    frappe.get_doc("DocType", "Absenteeism")
                    print("Doctype already exists:", "Absenteeism")

                    try:
                        newAbsenteeism = frappe.get_doc(
                            {
                                "doctype": "Absenteeism",
                                "employee": employee["name"],
                                "employee_name": employee["employee_name"],
                                "absent_date": date.today(),
                                "manager": manager["user_id"]
                            }
                        )
                        data = newAbsenteeism.insert()
                        frappe.db.commit()
                    except:
                        try:
                            newAbsenteeism = frappe.get_doc(
                            {
                                "doctype": "Absenteeism",
                                "employee": employee["name"],
                                "employee_name": employee["employee_name"],
                                "absent_date": date.today()
                            }
                            )
                            data = newAbsenteeism.insert()
                            frappe.db.commit()
                        except:
                            pass
                    try:
                        frappe.share.add("Absenteeism",data.name,employee["user_id"],1,1,0,0,0,1)
                    except:
                        print("share error for employee")
                    try:
                        frappe.share.add("Absenteeism",data.name,manager["user_id"],1,1,0,0,0,1)
                    except:
                        print("share error for manager")
                
                except frappe.DoesNotExistError:
                    print("Doctype already exists false:", "Absenteeism")
                