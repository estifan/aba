console.log("this is serviceworker")

self.addEventListener('push', (data) => {
    self.registration.showNotification('Hello world!', {
        body: data.data.text(),
      });
    console.log("working: ", JSON.stringify(data.data.text()))
});

// frappe.realtime.on('event_name', (data) => {
//     console.log(data)
// })


// const options = {
//     body: "notifcation from service worker",
//   };
//   self.Notification("service worker", options);