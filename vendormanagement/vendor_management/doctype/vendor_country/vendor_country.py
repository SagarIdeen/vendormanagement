import frappe
from frappe.model.document import Document
import requests
import json
from frappe.utils.background_jobs import enqueue

class Vendor_Country(Document):
    def on_update(self):
        # self.set_country()
        frappe.enqueue(self.set_country)

    def set_country(self):
        url = "http://35.154.0.123:82/api/method/vendormanagement.vendor_management.doctype.vendor_country.vendor_country.update_country"
        data = {
            "id": self.id,
            "country": self.country,
            "country_code": self.country_code
        }

        try:
            response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
            if response.status_code == 200:
                print("Country data updated on the external server.")
            else:
                print("Failed to update country data on the external server. Status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("An error occurred during the request:", e)

@frappe.whitelist(allow_guest=True)
def update_country():
    data = frappe.form_dict
    try:
        # Check if a Vendor_Country document with the given ID already exists
        existing_doc = frappe.get_all("Vendor_Country", filters={"country": data.get("country")})

        if existing_doc:
            # Update the existing document with the new data
            existing_doc = frappe.get_doc("Vendor_Country", existing_doc[0].name)
            existing_doc.id = data.get("id")
            existing_doc.country_code = data.get("country_code")
            existing_doc.save(ignore_permissions=True)
        else:
            # Create a new Vendor_Country document and enter the data into it
            new_doc = frappe.new_doc("Vendor_Country")
            new_doc.id = data.get("id")
            new_doc.country = data.get("country")
            new_doc.country_code = data.get("country_code")
            new_doc.insert(ignore_permissions=True)

        return "Country data updated or created successfully"
    except Exception as e:
        return "An error occurred while processing the request: " + str(e)

@frappe.whitelist()
def get_country_list():
    print("self")
    country_list = frappe.get_all("Vendor_Country", fields=["id", "country", "country_code"])
    return country_list
