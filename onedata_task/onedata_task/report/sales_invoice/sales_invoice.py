import frappe
from frappe.utils import flt, cint, getdate

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{"label": "Invoice Number", "fieldname": "name", "fieldtype": "Link", "options": "Sales Invoice", "width": 150},
		{"label": "Customer Name", "fieldname": "customer", "fieldtype": "Data", "width": 200},
		{"label": "Territory", "fieldname": "territory", "fieldtype": "Data", "width": 150},
		{"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
		{"label": "Total Amount", "fieldname": "grand_total", "fieldtype": "Currency", "width": 150},
	]

def get_data(filters):
	conditions = ""
	if filters.get("territory"):
		conditions += " AND territory = %(territory)s"
	if filters.get("from_date") and filters.get("to_date"):
		conditions += " AND posting_date BETWEEN %(from_date)s AND %(to_date)s"

	return frappe.db.sql(f"""
		SELECT 
			name, customer, territory, posting_date, grand_total
		FROM 
			`tabSales Invoice`
		WHERE 
			docstatus = 1 {conditions}
	""", filters, as_dict=True)
