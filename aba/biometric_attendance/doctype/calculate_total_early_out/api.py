import frappe

@frappe.whitelist()
def for_all_shifts(start_date,end_date):
    employees = frappe.get_all('Employee', filters={'status': 'Active'}, fields=['name', 'attendance_device_id', 'shift_type'])
    for employee in employees:
        Early_out = frappe.get_all('Early out', filters={'employee_id': employee['name'],"date": ["between",  (start_date, end_date)]}, fields=['name', 'early_time'])
        total = 0
        for early in Early_out :
            total = total + early["early_time"]
            
        frappe.db.set_value('Employee', employee['name'], 'early_out', round(total,1))
        print("total early out time: ",total)
    print(start_date,end_date)
    return ("Total early out calculation for all employee completed.")
    
    
    
    
