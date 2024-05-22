// Copyright (c) 2024, TTSP and contributors
// For license information, please see license.txt

frappe.ui.form.on("Calculate total Lateness", {
	calculate: function(frm) {
        console.log(frm.doc)
        frappe.call({
            method: "aba.biometric_attendance.doctype.calculate_total_lateness.api.for_all_shifts", 
            args: {
                start_date: frm.doc.start_date,
                end_date: frm.doc.end_date,
            },
            callback: function(r) {
                if (r.message) {
                    // Check if the message indicates progress
                    if (r.message.progress !== undefined) {
                        // Display progress in msgprint
                        frappe.msgprint("Progress: " + r.message.progress + "%", "Processing...", "info");
                    } else {
                        // Display final message
                        frappe.msgprint(r.message);
                    }
                }
                // frm.set_value('status',r['message'])
            }
        });
	}
});
