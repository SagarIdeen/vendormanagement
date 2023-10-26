# Copyright (c) 2023, Ideenkreice and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import json

class Vendor_Country(Document):
	def on_update(self):
		get_country()
@frappe.whitelist(allow_guest=True)
def get_country():
	url="http://35.154.0.123:8080/api/method/vendormanagement.vendor_management.doctype.vendor_country.vendor_country.get_country_list"
	response = requests.request("GET", url,headers = {
			'Content-Type': 'application/json',
				})
	response_data=response.json()
	for d in response_data["message"]:
			id = d["id"]
			if id:
				existing_doc = frappe.db.exists("Vendor_Country", {"id":id})
				
				if existing_doc:
					country = frappe.get_doc("Vendor_Country", existing_doc)
					if country.country != d['name']:
						print("country.country",d['name'],country.country)
						# frappe.rename_doc("demo_country",country.country, d['name'],merge=merge)
						
						# # # Update the existing document with new data
						# # country.country = d['name']
						# # # Update other fields as needed
						# # country.save(ignore_permissions=True)


				else:
					new_doc=frappe.new_doc("Vendor_Country")
					new_doc.id=d['id']
					new_doc.country=d['country']
					new_doc.country_code=d['country_code']
					new_doc.insert(ignore_permissions=True)

	return response_data

@frappe.whitelist(allow_guest=True)
def get_country_list():
	country_list=frappe.db.sql("""select * from `tabVendor_Country` """,as_dict=1)
	return country_list