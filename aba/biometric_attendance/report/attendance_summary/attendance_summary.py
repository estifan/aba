import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data

def get_columns():
    return [
        {
            "label": _("Employee ID"),
            "fieldname": "employee_id",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 110
        },
        {
            "label": _("Employee Name"),
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Date"),
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Type"),
            "fieldname": "type",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Check In Time"),
            "fieldname": "check_in_time",
            "fieldtype": "Time",
            "width": 100
        },
        {
            "label": _("Late Time"),
            "fieldname": "late_time",
            "fieldtype": "Float",
            "width": 100
        }
    ]

def get_data(filters):
    data = []

    include_lateness = filters.get("type") in [None, "", "Lateness"]
    include_absenteeism = filters.get("type") in [None, "", "Absenteeism"]

    if include_lateness:
        lateness_conditions = []
        lateness_values = []

        if filters.get("from_date"):
            lateness_conditions.append("date >= %s")
            lateness_values.append(filters["from_date"])
        if filters.get("to_date"):
            lateness_conditions.append("date <= %s")
            lateness_values.append(filters["to_date"])
        if filters.get("employee"):
            lateness_conditions.append("employee_id = %s")
            lateness_values.append(filters["employee"])

        lateness_where = " AND ".join(lateness_conditions) if lateness_conditions else "1=1"

        lateness_records = frappe.db.sql(f"""
            SELECT 
                employee_id,
                employee_name,
                date,
                'Lateness' as type,
                check_in_time,
                late_time
            FROM `tabLateness`
            WHERE {lateness_where}
            ORDER BY date DESC
        """, tuple(lateness_values), as_dict=1)

        data.extend(lateness_records)

    if include_absenteeism:
        absenteeism_conditions = []
        absenteeism_values = []

        if filters.get("from_date"):
            absenteeism_conditions.append("absent_date >= %s")
            absenteeism_values.append(filters["from_date"])
        if filters.get("to_date"):
            absenteeism_conditions.append("absent_date <= %s")
            absenteeism_values.append(filters["to_date"])
        if filters.get("employee"):
            absenteeism_conditions.append("employee = %s")
            absenteeism_values.append(filters["employee"])

        absenteeism_where = " AND ".join(absenteeism_conditions) if absenteeism_conditions else "1=1"

        absenteeism_records = frappe.db.sql(f"""
            SELECT 
                employee as employee_id,
                employee_name,
                absent_date as date,
                'Absenteeism' as type,
                NULL as check_in_time,
                NULL as late_time
            FROM `tabAbsenteeism`
            WHERE {absenteeism_where}
            ORDER BY absent_date DESC
        """, tuple(absenteeism_values), as_dict=1)

        data.extend(absenteeism_records)

    data.sort(key=lambda x: x.date, reverse=True)
    return data
