from time import sleep
from aba.biometric_attendance.device import hikvisionGetcheckIn
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
def update_absent_time_for_employees(device, start_date, end_date, start_time, time_to_wait, has_exceptional_day, e_day, e_start_time, e_time_to_wait, abashift_id):
    device_doc = frappe.db.get_value('Device', device, ['ip_address', 'user_name', 'password']) 
    
    # # Retrieve all employees
    employees = frappe.get_all('Employee', filters={'status': 'Active','shift_type':abashift_id}, fields=['name', 'attendance_device_id', 'shift_type',"employee_name","name","user_id","reports_to"])

    total_employees = len(employees)
    processed_employees = 0

    for employee in employees:
        #employee_number = frappe.db.get_value('Employee', employee.first_name, 'attendance_device_id')
        update_progress(processed_employees, total_employees)
        employee_number=employee['attendance_device_id']
        print(employee_number)
        absent_time = calculate_absent_time(device_doc, employee, start_date, end_date, start_time, time_to_wait, has_exceptional_day, e_day, e_start_time, e_time_to_wait)
        
        processed_employees += 1
        # # Update the specific field in the employee's doctype with the calculated absent time
        # frappe.db.set_value('Employee', employee['name'], 'absent_time', absent_time)

    update_progress(total_employees, total_employees)
    return ("Absent time set for all employees")


def requestChecker(attendance_url,headers,payload,Hikivision_Username,Hikivision_Password):
    attendance_response = requests.post(
            attendance_url,
            headers=headers,
            data=payload,
            auth=HTTPDigestAuth(Hikivision_Username, Hikivision_Password)
        )
    if attendance_response.status_code != 200:
            print("error")
            sleep(10)
            print("sleep done")
            return requestChecker(attendance_url,headers,payload,Hikivision_Username,Hikivision_Password)
    else:
        return attendance_response

def calculate_absent_time(device_doc, employee, start_date, end_date, start_time, time_to_wait, has_exceptional_day, e_day, e_start_time, e_time_to_wait):
    def attendance(Hikivision_Username, Hikivision_Password, Hikivision_IP, employeeNo, day):
        attendance_url = f"http://{Hikivision_IP}/ISAPI/AccessControl/AcsEvent?format=json"
        payload = json.dumps({
            "AcsEventCond": {
                "searchID": f"{employeeNo}",
                "searchResultPosition": 0,
                "maxResults": 1,
                "major": 5,
                "minor": 38,
                "startTime": f"{day}T06:00:49+03:00",
                "endTime": f"{day}T18:00:49+03:00",
                "employeeNoString": f"{employeeNo}"
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        attendance_response = requestChecker(attendance_url,headers,payload,Hikivision_Username,Hikivision_Password)
        attendance_data = attendance_response.json()
        checkIn_Time = attendance_data["AcsEvent"]
        return checkIn_Time

    count = timedelta(hours=0)
    delta = timedelta(days=1)
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    exception_day = exc_date(e_day)
    weekDay = start_date.weekday() + 1

    while start_date <= end_date:
        data = attendance(device_doc[1], device_doc[2], device_doc[0], employee['attendance_device_id'], datetime.strftime(start_date, '%Y-%m-%d'))
        print("data:",data)
        if data['totalMatches'] != 0:
            data = data["InfoList"][0]["time"]
            if data:
                start_time1 = datetime.strptime(start_time, '%H:%M:%S')
                time_to_wait1 = datetime.strptime(time_to_wait, '%H:%M:%S')
                if has_exceptional_day:
                    if weekDay >= 7:
                        
                        if start_date.weekday() == 6:
                            print(start_date.weekday())
                            weekDay = 0
                        else:
                            weekDay = 1
                    print("exception: ",weekDay == exception_day)
                    print("start_date",start_date)
                    print("weekDay: ",weekDay)
                    if weekDay == exception_day:
                        start_time1 = datetime.strptime(e_start_time, '%H:%M:%S')
                        time_to_wait1 = datetime.strptime(e_time_to_wait, '%H:%M:%S')
                        # weekDay = weekDay - 7
                        # print("weekDay negative: ",weekDay)
                    
                    
                    
                compare_Time = start_time1 + (time_to_wait1 - datetime(1900, 1, 1))
                compare_Time = datetime.strftime(compare_Time, '%H:%M:%S')
                compare_Time = datetime.strptime(compare_Time, '%H:%M:%S').time()
                checkIn_Time = datetime.fromisoformat(data).time()
                print("compare_Time: ",compare_Time)
                
                if checkIn_Time > compare_Time:
                    if weekDay == 0:
                        start_date += delta
                        weekDay = weekDay + 1
                        next
                    final = datetime.combine(date.today(), checkIn_Time) - datetime.combine(date.today(), start_time1.time())
                    # count = count + final
                    # print("count: ",count)
                    latenessOfTheDay = final.total_seconds() / 3600
                    latenessRecord = frappe.get_all('Lateness', filters={'name': f'{start_date.date()}-{employee["employee_name"]}'}, fields=['check_in_time', 'late_time','workflow_state'])
                    print(len(latenessRecord))
                    if(len(latenessRecord) == 0):
                        manager = {}
                        if(employee["reports_to"]): 
                            manager = frappe.get_all('Employee', filters={'status': 'Active','name':  employee["reports_to"]}, fields=["user_id"])[0]
                        try:
                            try:
                                newLateness = frappe.get_doc(
                                    {
                                        "doctype": "Lateness",
                                        "employee_id": employee["name"],
                                        "employee_name": employee["employee_name"],
                                        "date": start_date.date(),
                                        "check_in_time": checkIn_Time,
                                        "late_time": latenessOfTheDay,
                                        # "employee_email": employee["user_id"],
                                        "manager": manager["user_id"],
                                        # "owner": managerUser["username"],
                                    }
                                )
                                data = newLateness.insert()
                                frappe.db.commit()
                            except:
                                newLateness = frappe.get_doc(
                                    {
                                        "doctype": "Lateness",
                                        "employee_id": employee["name"],
                                        "employee_name": employee["employee_name"],
                                        "date": start_date.date(),
                                        "check_in_time": checkIn_Time,
                                        "late_time": latenessOfTheDay,
                                        # "employee_email": employee["user_id"],
                                        # "manager": manager["user_id"],
                                        # "owner": managerUser["username"],
                                    }
                                )
                                data = newLateness.insert()
                                frappe.db.commit()
                            # #change doc owner
                            # frappe.db.set_value("Lateness", data.name, "owner", managerUser["username"])
                            # print("doc data:", data.name)
                            #assign user
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
                        except Exception as error:
                            print("error: ",error)
                        print("final: ",final)
                    # elif(latenessRecord["workflow_state"]=="Pending"):

                    else:
                        print("already exists")
                else:
                    pass
            else:
                pass
        start_date += delta
        weekDay = weekDay + 1
    
    return True

def update_progress(processed, total):
    progress = int((processed / total) * 100)
    frappe.publish_progress(float(progress), ('Processing...'), 'info')