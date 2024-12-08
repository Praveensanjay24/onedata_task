import json
import frappe

@frappe.whitelist()
def bulk_convert_leads(leads):
	if isinstance(leads, str):
		try:
			leads = json.loads(leads)
		except json.JSONDecodeError:
			frappe.throw(_("Invalid leads list format. Please provide a valid list of leads."))

	if not leads or not isinstance(leads, list):
		frappe.throw(_("Invalid leads list. Please provide a valid list of leads."))

	converted = []
	for lead_name in leads:
		try:
			lead = frappe.get_doc("Lead", lead_name)
			if lead.status != "Converted":
				customer = frappe.new_doc("Customer")
				customer.customer_name = lead.lead_name
				customer.customer_type = "Individual"
				customer.customer_group = "Individual"
				customer.territory = "India"
				customer.insert(ignore_permissions=True)

				lead.status = "Converted"
				lead.customer = customer.name
				lead.save(ignore_permissions=True)

				converted.append(lead.name)
		except frappe.DoesNotExistError:
			frappe.log_error(f"Lead {lead_name} not found.", "Bulk Convert Leads")
		except Exception as e:
			frappe.log_error(f"Error converting lead {lead_name}: {str(e)}", "Bulk Convert Leads")

	return {"converted_leads": converted}
