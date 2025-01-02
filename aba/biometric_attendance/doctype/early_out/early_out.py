# Copyright (c) 2024, TTSP and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from aba.biometric_attendance.device import hikvisionGetCheckOut
import frappe
from datetime import date, datetime
from frappe.model.document import Document


class Earlyout(Document):
	def before_save(self):
		print("workflow_state",self.workflow_state)
		frappe.get_roles
		if(self.workflow_state == "Approved"):
			self.early_time = 0.00
		elif(self.workflow_state == "Waiting For Manager Approval"):
			employee = frappe.get_all('Employee', filters={"name": self.employee_id }, fields=['shift_type',"user_id"])[0]
			if frappe.get_user().doc.name != employee['user_id'] and frappe.get_user().doc.name != "Administrator": 
				self.workflow_state = "Pending"
				frappe.msgprint("You can't request approval for other employee","Error")
			else:
				self.check_out_time = "17:40:00"
		elif(self.workflow_state == "Waiting For HR Approval"):
			employee = frappe.get_all('Employee', filters={"name": self.employee_id }, fields=['shift_type',"user_id"])[0]
			print("Waiting For HR Approval",frappe.get_user().doc.name)
			if frappe.get_user().doc.name == employee['user_id']:
				self.workflow_state = "Waiting For Manager Approval"
				frappe.msgprint("You can't approve you own request.","Error")
		elif(self.workflow_state == "Rejected"):
			print("Rejected")
			employee = frappe.get_all('Employee', filters={"name": self.employee_id }, fields=['shift_type',"user_id","attendance_device_id"])[0]
			shift = frappe.get_all('ABAshift', filters={'name': employee['shift_type']}, fields=['name','device'])[0]
			print("shift: ",shift)
			check_out_time =hikvisionGetCheckOut(employeeNo=employee['attendance_device_id'],day= self.date, device=shift["device"])
			self.check_out_time = check_out_time 
