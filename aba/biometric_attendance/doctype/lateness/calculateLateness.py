
import frappe
from datetime import date, datetime, timedelta

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


def calculateLateness(start_date = date.today(), end_date = date.today(),abashift_id = "null",chackIn=""):
    shiftData  = frappe.db.get_values("ABAshift", {'name': abashift_id}, "*", as_dict=True)[0]
    print(shiftData)


    count = timedelta(hours=0)
    delta = timedelta(days=1)
    start_date = start_date
    end_date = end_date
    exception_day = exc_date(shiftData["e_day"])
    weekDay = start_date.weekday() + 1

    while start_date <= end_date:
                start_time1 = datetime.strptime(str(shiftData["start_time"]), '%H:%M:%S')
                time_to_wait1 = datetime.strptime(str(shiftData["time_to_wait"]), '%H:%M:%S')
                if shiftData["has_exceptional_day"]:
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
                        start_time1 = datetime.strptime(shiftData["e_start_time"], '%H:%M:%S')
                        time_to_wait1 = datetime.strptime(shiftData["e_time_to_wait"], '%H:%M:%S')
                        # weekDay = weekDay - 7
                        # print("weekDay negative: ",weekDay)
                    
                    
                    
                compare_Time = start_time1 + (time_to_wait1 - datetime(1900, 1, 1))
                compare_Time = datetime.strftime(compare_Time, '%H:%M:%S')
                compare_Time = datetime.strptime(compare_Time, '%H:%M:%S').time()
                checkIn_Time = chackIn
                print("compare_Time: ",compare_Time)
                
                if checkIn_Time > compare_Time:
                    if weekDay == 0:
                        start_date += delta
                        weekDay = weekDay + 1
                        next
                    if checkIn_Time <= datetime.strptime("12:00:00", '%H:%M:%S').time():
                        final = datetime.combine(date.today(), checkIn_Time) - datetime.combine(date.today(), start_time1.time())
                        count = count + final
                        print("count: ",count)
                        print("final: ",final)
                else:
                    pass
                start_date += delta
                weekDay = weekDay + 1
    rounded_count = round(count.total_seconds() / 3600, 1)
    print("lateness: ", rounded_count)
    return rounded_count 