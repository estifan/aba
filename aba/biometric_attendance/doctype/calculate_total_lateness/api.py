import frappe

@frappe.whitelist()
def for_all_shifts(start_date,end_date):
    employees = frappe.get_all('Employee', filters={'status': 'Active'}, fields=['name', 'attendance_device_id', 'shift_type'])
    for employee in employees:
        Lateness = frappe.get_all('Lateness', filters={'employee_id': employee['name'],"date": ["between",  (start_date, end_date)]}, fields=['name', 'late_time'])
        total = 0
        for Late in Lateness:
            total = total + Late["late_time"]
            
        frappe.db.set_value('Employee', employee['name'], 'absent_time', round(total,1))
        print("total late time: ",total)
    print(start_date,end_date)
    return ("Total lateness calculation for all employee complied.")
    
    
    
    
