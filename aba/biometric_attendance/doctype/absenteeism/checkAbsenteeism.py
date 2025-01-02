from time import sleep
from aba.biometric_attendance.device import hikvisionGetAbsenteeism
import frappe
import requests
from requests.auth import HTTPDigestAuth
import json
from datetime import datetime, date, time, timedelta
import frappe.share

def exc_date(day):
    switcher = {
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6,
        "Sunday": 7,
    }

    return switcher.get(day, 'Invalid choice')

@frappe.whitelist()
def update_absent_time_for_employees(device, start_date, end_date,abashift_id):
    
    # # Retrieve all employees
    employees = frappe.get_all('Employee', filters={'status': 'Active','shift_type':abashift_id}, fields=['name', 'attendance_device_id', 'shift_type',"employee_name","name","user_id","reports_to"])

    total_employees = len(employees)
    processed_employees = 0
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    delta = timedelta(days=1)
    for employee in employees:
        start_date_loop =  datetime.strptime(start_date, '%Y-%m-%d')
        #employee_number = frappe.db.get_value('Employee', employee.first_name, 'attendance_device_id')
        update_progress(processed_employees, total_employees)
        employee_number=employee['attendance_device_id']
        print(employee_number)
        while start_date_loop <= end_date:
            shift = frappe.get_doc('ABAshift', employee['shift_type']).as_dict()
            if len(shift.list_of_days):
                filtered_arr = [d for d in shift.list_of_days if exc_date(d.day_of_the_week)-1 == start_date_loop.weekday()]
                if len(filtered_arr):
                    print("day_of_the_week: ",filtered_arr[0].day_of_the_week)
                    start_date_loop += delta
                    continue
            leave = frappe.get_all('Attendance', filters={"status":"On Leave",'attendance_date': date.today(),"employee": employee['name']}, fields=['name'])
            print("leave", leave)
            if len(leave):
                continue
            start_date_loop2 = datetime.strftime(start_date_loop,'%Y-%m-%d')
            Absenteeism = hikvisionGetAbsenteeism(employeeNo= employee['attendance_device_id'],device=device,day= start_date_loop2)
            manager = {}
            if(employee["reports_to"]): 
                manager = frappe.get_all('Employee', filters={'status': 'Active','name':  employee["reports_to"]}, fields=["user_id"])[0]
            print("Absenteeism: ",Absenteeism)
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
                                "absent_date": start_date_loop2,
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
                                "absent_date": start_date_loop2
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
            start_date_loop += delta
        processed_employees += 1
        update_progress(processed_employees, total_employees)
        # # Update the specific field in the employee's doctype with the calculated absent time
        # frappe.db.set_value('Employee', employee['name'], 'absent_time', absent_time)

    return ("Absenteeism check completed")


def update_progress(processed, total):
    progress = int((processed / total) * 100)
    frappe.publish_progress(float(progress), ('Processing...'), 'info')