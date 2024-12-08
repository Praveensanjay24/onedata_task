frappe.listview_settings['Lead'] = {
    onload: function (listview) {
        listview.page.add_actions_menu_item(__('Bulk Convert to Customers'), function () {
            let selected_items = listview.get_checked_items();
            if (!selected_items.length) {
                frappe.msgprint('Please select at least one Lead.');
                return;
            }
            const lead_names = selected_items.map(item => item.name);
            frappe.call({
                method: 'onedata_task.custom.bulk_convert_leads',
                args: {
                    leads: lead_names
                },
                callback: function (response) {
                    if (response.message) {
                        frappe.msgprint(__('Leads converted to customers successfully.'));
                        listview.refresh();
                    }
                }
            });
        });
    }
};
