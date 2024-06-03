// frappe.provide("frappe");
// var cssId = "myCss"; // you could encode the css path itself to generate id..
// if (!document.getElementById(cssId)) {
//   var head = document.getElementsByTagName("head")[0];
//   var link = document.createElement("link");
//   link.id = cssId;
//   link.rel = "manifest";
//   link.href = "http://192.168.1.18:8000/assets/aba/manifest.json";
//   link.media = "all";
//   head.appendChild(link);
// }

// console.log("email: ", frappe.session);
// Notification.requestPermission().then(async (result) => {
//   if (result === "granted") {
//     const options = {
//       body: "notifBody",
//     };
//     if ("serviceWorker" in navigator) {
//       navigator.serviceWorker
//         .register("/assets/aba/service_worker.js")
//         .then(async (sw) => {
//           window.addEventListener("load", async () => {
//             if (sw.active) {
//               let push = await sw.pushManager.subscribe({
//                 userVisibleOnly: true,
//                 applicationServerKey:
//                   "BBZY7Q3KEtZArAAWMLi_qzWHbH4vAoqPpIXnRhmlUaw0PVs1Kt_2fgLhuaVI5i8MWASBKx3d6W6UoH2U3qChw9U",
//               });
//               console.log("push", push.toJSON());
//               frappe.call({
//                 method: "aba.aba.doctype.notification_push_manager.api.addSub",
//                 args: {
//                   user: frappe.session.user_email,
//                   endpoint: push.endpoint,
//                   auth: push.toJSON().keys.auth,
//                   p256dh: push.toJSON().keys.p256dh,
//                 },
//                 callback: function (r) {
//                   if (r.message) {
//                     console.log(r.message);
//                   }
//                 }
//               });
//             }
//           });
//         });
//     }
//   }
// });
