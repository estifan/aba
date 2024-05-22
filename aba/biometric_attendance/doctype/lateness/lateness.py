# Copyright (c) 2024, TTSP and contributors
# For license information, please see license.txt

# import frappe
import frappe
from datetime import date, datetime
from frappe.model.document import Document


class Lateness(Document):
	def before_save(self):
		print("workflow_state",self.workflow_state)
		frappe.get_roles
		if(self.workflow_state == "Approved"):
			employee = frappe.get_all('Employee', filters={"name": self.employee_id }, fields=['shift_type',"user_id"])[0]
			shift = frappe.get_all('ABAshift', filters={"name": employee['shift_type'] }, fields=['start_time'])[0]
			if(self.check_in_time >= shift["start_time"]):
				late_time = self.check_in_time - shift["start_time"]
				print("late_time: ", late_time)
				rounded_late_time = round(late_time.total_seconds() / 3600, 1)
				self.late_time = rounded_late_time
				print("rounded_late_time: ", rounded_late_time)
				# print("compare",self.check_in_time >= shift["start_time"])
			else:
				self.late_time = 0.00
			# print("late agan",)
		elif(self.workflow_state == "Waiting For HR Approval"):
			employee = frappe.get_all('Employee', filters={"name": self.employee_id }, fields=['shift_type',"user_id"])[0]
			print("Waiting For HR Approval",frappe.get_user().doc.name)
			if frappe.get_user().doc.name == employee['user_id']:
				self.workflow_state = "Waiting For Manager Approval"
				frappe.msgprint("You can't approve you own request.","Error")
		elif(self.workflow_state == "Rejected"):
			print("Rejected")
