frappe.ui.form.on('Lead', {
	before_save: function (frm) {
		let phone_number = frm.doc.phone;
		let regex = /^\+\d+/;

		if (!phone_number.match(regex)) {
			frappe.throw(__('Phone number must start with a valid country code (e.g., +1, +91)'));
		}

		if (phone_number.length > 15) {
			frappe.throw(__('Phone number must not exceed 15 characters.'));
		}
	}
});
