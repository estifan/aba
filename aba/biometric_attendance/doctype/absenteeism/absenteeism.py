# Copyright (c) 2024, TTSP and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document


class Absenteeism(Document):
	def before_save(self):
		print("workflow_state",self.workflow_state)
		frappe.get_roles
		if(self.workflow_state == "Approved"):
			self.deductible = "No"
			pass
		elif(self.workflow_state == "Waiting For Manager Approval"):
			employee = frappe.get_all('Employee', filters={"name": self.employee }, fields=['shift_type',"user_id"])[0]
			if frappe.get_user().doc.name != employee['user_id'] or frappe.get_user().doc.name == "Administrator":
				self.workflow_state = "Pending"
				frappe.msgprint("You can't request approval for other employee","Error")
			# else:
			# 	self.check_in_time = "8:00:00"
		elif(self.workflow_state == "Waiting For HR Approval"):
			employee = frappe.get_all('Employee', filters={"name": self.employee }, fields=['shift_type',"user_id"])[0]
			print("Waiting For HR Approval",frappe.get_user().doc.name)
			if frappe.get_user().doc.name == employee['user_id']:
				self.workflow_state = "Waiting For Manager Approval"
				frappe.msgprint("You can't approve you own request.","Error")
		elif(self.workflow_state == "Rejected"):
			pass
			# to do
