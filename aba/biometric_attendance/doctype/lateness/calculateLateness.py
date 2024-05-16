
import frappe


def calculateLateness(start_date, end_date,abashift_id):
    shiftData  = frappe.get_all('abashift',filters={'name': abashift_id})
    print(shiftData)