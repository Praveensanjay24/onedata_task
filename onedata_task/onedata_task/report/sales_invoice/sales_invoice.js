frappe.query_reports['Sales Invoice'] = {
    filters: [
        {
            fieldname: 'territory',
            label: __('Territory'),
            fieldtype: 'Link',
            options: 'Territory',
            reqd: 0  // Set to 1 if the filter is mandatory
        },
        {
            fieldname: 'from_date',
            label: __('From Date'),
            fieldtype: 'Date',
            reqd: 0
        },
        {
            fieldname: 'to_date',
            label: __('To Date'),
            fieldtype: 'Date',
            reqd: 0
        }
    ]
};
