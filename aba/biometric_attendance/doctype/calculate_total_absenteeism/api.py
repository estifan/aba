import frappe

@frappe.whitelist()
def for_all_shifts(start_date,end_date):
    employees = frappe.get_all('Employee', filters={'status': 'Active'}, fields=['name', 'attendance_device_id', 'shift_type'])
    print("employees: ", employees)
    for employee in employees:
        Absenteeism = frappe.get_all('Absenteeism', filters={'employee': employee['name'],"absent_date": ["between",  (start_date, end_date)]}, fields=['name','deductible'])    
        print("Absenteeism: ", Absenteeism)
        frappe.db.set_value('Employee', employee['name'], 'Absenteeism',len(Absenteeism))
        print("total late time: ")
    print(start_date,end_date)
    return ("Total Absenteeism calculation for all employee completed.")
    
    
    
    
