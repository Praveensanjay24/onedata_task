import json
import frappe
import requests

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



@frappe.whitelist()
def get_weather_data(city):
	api_key = "ce763d199c8393fbd37a8171a4985b30"
	if not api_key:
		frappe.throw("Weatherstack API key is not configured.")

	url = f"http://api.weatherstack.com/current"
	params = {
		"access_key": api_key,
		"query": city
	}

	try:
		response = requests.get(url, params=params)
		response.raise_for_status()
		data = response.json()

		if 'error' in data:
			frappe.throw(data['error'].get('info', 'An error occurred while fetching weather data.'))

		current = data.get("current", {})
		temperature = current.get("temperature")
		weather_desc = current.get("weather_descriptions", [])[0] if current.get("weather_descriptions") else ""
		observation_time = current.get("observation_time")

		weather_doc = frappe.new_doc("Weather Data")
		weather_doc.city = city
		weather_doc.temperature = temperature
		weather_doc.weather_description = weather_desc
		weather_doc.observation_time = observation_time
		weather_doc.insert(ignore_permissions=True)

		return {"message": "Weather data saved successfully.", "data": weather_doc.as_dict()}

	except requests.exceptions.RequestException as e:
		frappe.log_error(message=str(e), title="Weatherstack API Error")
		frappe.throw("Failed to fetch weather data. Please try again later.")