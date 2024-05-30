// Copyright (c) 2024, TTSP and contributors
// For license information, please see license.txt

frappe.ui.form.on("Notification Push Manager", {
  refresh(frm) {},

  test_notification(frm) {
    frappe.call({
      method: "aba.aba.doctype.notification_push_manager.push.push",
      args: {
        endpoint: frm.doc.endpoint,
        p256dh: frm.doc.p256dh,
        auth: frm.doc.auth,
        user: frm.doc.user,
        data: "test notification",
      },
      callback: function (r) {
        console.log(r.message);
      },
    });
  },
});
