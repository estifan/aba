from aba.biometric_attendance.doctype.lateness.calculateLateness import calculateLateness, exc_date
import frappe
import requests
from requests.auth import HTTPDigestAuth
import json
import frappe.share
from datetime import datetime, date, time, timedelta
from aba.biometric_attendance.device import hikvisionGetcheckIn
from frappe.desk.form.assign_to import add

def addDailyLatenessToDoc():
    print("daily")
    employees = frappe.get_all('Employee', filters={'status': 'Active'}, fields=['name', "employee_name","user_id", 'attendance_device_id','shift_type','reports_to'])
    # print(employees)
    # frappe.delete_doc("Check In", "2024-05-15-Nebyou ame")
    # a = frappe.get_all('Lateness')
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
            checkIn_Time = hikvisionGetcheckIn(employeeNo= employee['attendance_device_id'],device=shift["device"])
            manager = {}
            if(employee["reports_to"]): 
                manager = frappe.get_all('Employee', filters={'status': 'Active','name':  employee["reports_to"]}, fields=["user_id"])[0]
            print(checkIn_Time)
            try:
                frappe.get_doc("DocType", "Lateness")
                print("Doctype already exists:", "Lateness")
                lateTime = calculateLateness(abashift_id=employee['shift_type'],chackIn=checkIn_Time)
                if(lateTime):
                    try:
                        newLateness = frappe.get_doc(
                            {
                                "doctype": "Lateness",
                                "employee_id": employee["name"],
                                "employee_name": employee["employee_name"],
                                "date": date.today(),
                                "check_in_time": checkIn_Time,
                                "late_time": lateTime,
                                "manager": manager["user_id"],
                                # "employee_email": employee["user_id"],
                                # "manager_email": manager["user_id"],
                                # "owner": managerUser["username"],
                            }
                        )
                        data = newLateness.insert()
                        frappe.db.commit()
                    except:
                        try:
                            newLateness = frappe.get_doc(
                            {
                                "doctype": "Lateness",
                                "employee_id": employee["name"],
                                "employee_name": employee["employee_name"],
                                "date": date.today(),
                                "check_in_time": checkIn_Time,
                                "late_time": lateTime,
                                # "manager": manager["user_id"],
                                # "employee_email": employee["user_id"],
                                # "manager_email": manager["user_id"],
                                # "owner": managerUser["username"],
                            }
                            )
                            data = newLateness.insert()
                            frappe.db.commit()
                        except:
                            pass
                    # #change doc owner
                    # frappe.db.set_value("Lateness", data.name, "owner", managerUser["username"])
                    # print("doc data:", data.name)
                    #assigne user
                    # args = {
                    #     "assign_to" : [],
                    #     "doctype" : "Lateness",
                    #     "name" : data.name,
                    #     "description" : "auto assignment",
                    # }
                    # add(args, ignore_permissions=True)
                    try:
                        frappe.share.add("Lateness",data.name,employee["user_id"],1,1,0,0,0,1)
                    except:
                        print("share error for employee")
                    try:
                        frappe.share.add("Lateness",data.name,manager["user_id"],1,1,0,0,0,1)
                    except:
                        print("share error for manager")
                
            except frappe.DoesNotExistError:
                print("Doctype already exists false:", "Lateness")
            