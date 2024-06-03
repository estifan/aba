import frappe
import requests
from requests.auth import HTTPDigestAuth
import json
from datetime import datetime, date

def hikvisionGetcheckIn(employeeNo,day = datetime.strftime(date.today(), '%Y-%m-%d'),device="ABA-Hikvision"):
    device_doc = frappe.db.get_value('Device', device, ['ip_address', 'user_name', 'password'])
    print("Geting.. check in")

    Hikivision_Username = device_doc[1]
    Hikivision_Password = device_doc[2]
    Hikivision_IP = device_doc[0]

    attendance_url = f"http://{Hikivision_IP}/ISAPI/AccessControl/AcsEvent?format=json"
    # "timeReverseOrder":
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

    attendance_response = requests.post(
        attendance_url,
        headers=headers,
        data=payload,
        auth=HTTPDigestAuth(Hikivision_Username, Hikivision_Password)
    )

    if attendance_response.status_code != 200:
        print("error: ",attendance_response)
        hikvisionGetcheckIn(employeeNo,day,device)
        # return False
    
    attendance_data = attendance_response.json()
    data = attendance_data["AcsEvent"]
    if data['totalMatches'] != 0:
        data = data["InfoList"][0]["time"]
        if data:
            checkIn_Time = datetime.fromisoformat(data).time()
    return checkIn_Time