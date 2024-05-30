frappe.provide("frappe");
var cssId = "myCss"; // you could encode the css path itself to generate id..
if (!document.getElementById(cssId)) {
  var head = document.getElementsByTagName("head")[0];
  var link = document.createElement("link");
  link.id = cssId;
  link.rel = "manifest";
  link.href = "http://192.168.1.18:8000/assets/aba/manifest.json";
  link.media = "all";
  head.appendChild(link);
}

console.log("email: ", frappe.session);
Notification.requestPermission().then(async (result) => {
  if (result === "granted") {
    const options = {
      body: "notifBody",
    };
    // new Notification("notifTitle", options);
    ////////
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker
        .register("/assets/aba/service_worker.js")
        .then(async (sw) => {
        //   window.addEventListener("load", async () => {
            if (sw.active) {
              let push = await sw.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey:
                  "BBZY7Q3KEtZArAAWMLi_qzWHbH4vAoqPpIXnRhmlUaw0PVs1Kt_2fgLhuaVI5i8MWASBKx3d6W6UoH2U3qChw9U",
              });
              console.log("push", push.toJSON());
              frappe.call({
                method: "aba.aba.doctype.notification_push_manager.api.addSub",
                args: {
                  user: frappe.session.user_email,
                  endpoint: push.endpoint,
                  auth: push.toJSON().keys.auth,
                  p256dh: push.toJSON().keys.p256dh,
                },
                callback: function (r) {
                  if (r.message) {
                    console.log(r.message);
                  }
                }
              });
            }
        //   });
        });
    }
  }
});


// async function subscribe() {
//     let sw = await navigator.serviceWorker.ready;

// }

// frappe.provide('frappe.realtime');

// frappe.realtime.on('notification2', function (data){
//     console.log("data not:",data)
// })
// frappe.realtime.off("doc_viewers");
// frappe.realtime.on("doc_viewers", function (data) {
//     console.log("service worker",data)
// });
// console.log(frappe)

// Copyright (c) 2019, Frappe Technologies and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Notification Log", {
// 	refresh: function (frm) {
//         console.log(frm.doc)
//         if(frm.doc.for_user == frappe.user.name){

//             const options = {
//                 body: "notifBody",
//             };
//             new Notification("notifTitle", options);
//         }
//     },

// 	after_save: function(frm){
//         if(frm.doc.for_user == frappe.user.name){

//             const options = {
//                 body: "notifBody",
//             };
//             new Notification("notifTitle", options);
//         }
//         console.log(frm.doc.for_user == frappe.user.name)
//     },

// });
