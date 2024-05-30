
frappe.views.calendar['Lateness'] = {
    field_map: {
        start: 'date',
        end: 'date',
        id: 'name',
        allDay: 'all_day',
        title: 'employee_name'
        // status: 'event_type',
        // color: 'color'
    },
    // style_map: {
    //     Public: 'success',
    //     Private: 'info'
    // },
    // order_by: 'check_in_time',
    // get_events_method: 'frappe.desk.doctype.event.event.get_events'
}
