frappe.ui.form.on('Weather Data', {
    refresh: function(frm) {
        frm.add_custom_button(__('Fetch Weather'), function() {
            frappe.prompt('Enter City Name', ({ value }) => {
                frappe.call({
                    method: 'onedata_task.custom.get_weather_data',
                    args: { city: value },
                    callback: function(response) {
                        if (response.message) {
                            frappe.msgprint(response.message.message);
                            frm.reload_doc();
                        }
                    }
                });
            });
        });
    }
});
