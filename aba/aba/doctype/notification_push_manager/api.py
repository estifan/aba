import frappe


@frappe.whitelist()
def addSub(user,endpoint,auth,p256dh):
    data = frappe.db.get_value('Notification Push Manager', user, ['user','endpoint'])
    print(data)
    if(data == None):
        newLateness = frappe.get_doc(
            {
                "doctype": "Notification Push Manager",
                "user": user,
                "endpoint": endpoint,
                "auth": auth,
                "p256dh": p256dh,
            }
        )
        data = newLateness.insert()
        frappe.db.commit()
    else:
        frappe.db.set_value('Notification Push Manager', user,{'endpoint':endpoint,'auth':auth,'p256dh':p256dh})
        print("update")

    return "sub added to doctype."