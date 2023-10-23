# Copyright (c) 2023, Ideenkreice and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class VendorCity(Document):
	pass
# @frappe.whitelist()
# def get_city():
# 	city=frappe.db.sql("""select * from `tabvendor_demo_city` where country='India' """,as_dict=1)
# 	for d in city:
# 		state=d['state']+'-'+d['state_id']
		
# 		new_doc=frappe.new_doc("Vendor City")
# 		new_doc.city=d['city']
# 		new_doc.city_id=d['city_id']
# 		new_doc.state=state
# 		new_doc.state_id=d['state_id']
# 		new_doc.state_code=d['state_code']
# 		new_doc.country_id=d['country_id']
# 		new_doc.country =d['country']
# 		new_doc.country_code=d['country_code']
		

# 		new_doc.insert(ignore_permissions=True)
# 	return city
@frappe.whitelist(allow_guest=True)
def get_city():
	url="http://35.154.0.123:8080/api/method/vendormanagement.vendor_management.doctype.vendor_country.vendor_country.get_city_list"
	response = requests.request("GET", url,headers = {
			'Content-Type': 'application/json',
				})
	response_data=response.json()
	for d in response_data["message"]:
			city_id = d["city_id"]
			if id:
				existing_doc = frappe.db.exists("Vendor City", {"city_id":city_id})
				
				if existing_doc:
					country = frappe.get_doc("Vendor City", existing_doc)
					# if country.country != d['name']:
					# 	print("country.country",d['name'],country.country)
						


				else:
					new_doc=frappe.new_doc("Vendor City")
					new_doc.city_id=d['city_id']
					new_doc.city=d['city']
					new_doc.state=d['state']
					new_doc.country=d['country']
					new_doc.insert(ignore_permissions=True)

	return response_data

@frappe.whitelist(allow_guest=True)
def get_city_list():
	city_list=frappe.db.sql("""select * from `tabVendor City` """,as_dict=1)
	return city_list