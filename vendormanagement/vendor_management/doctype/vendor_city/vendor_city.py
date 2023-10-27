# Copyright (c) 2023, Ideenkreice and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import json
import re

class VendorCity(Document):
	def on_update(self):
		self.set_cities()
	def set_cities(self):
		url = "http://35.154.0.123:82/api/method/vendormanagement.vendor_management.doctype.vendor_city.vendor_city.update_city"
        data = {
			"city_id":self.city_id,
			"city":self.city,
			"state":self.state,
			"country": self.country
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
def update_city():
    data = frappe.form_dict
    try:
        # Check if a Vendor_Country document with the given ID already exists
        existing_doc = frappe.get_all("Vendor City", filters={"city_id": data.get("city_id")})

        if existing_doc:
            # Update the existing document with the new data
            existing_doc = frappe.get_doc("Vendor City", existing_doc[0].name)
			existing_doc.city = data.get("city")
            existing_doc.state = data.get("state")
            existing_doc.country = data.get("country")
            existing_doc.save(ignore_permissions=True)
        else:
            # Create a new Vendor_Country document and enter the data into it
            new_doc = frappe.new_doc("Vendor City")
            new_doc.state = data.get("state")
			new_doc.city_id = data.get("city_id")
			new_doc.city = data.get("city")
			new_doc.country= data.get("country")
           
            new_doc.insert(ignore_permissions=True)

        return "Country data updated or created successfully"
    except Exception as e:
        return "An error occurred while processing the request: " + str(e)
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
# @frappe.whitelist(allow_guest=True)
# def get_cities():
# 	url="http://35.154.0.123:8080/api/method/vendormanagement.vendor_management.doctype.vendor_city.vendor_city.get_city_list"
# 	response = requests.request("GET", url,headers = {
# 			'Content-Type': 'application/json',
# 				})
# 	response_data=response.json()
# 	print("response_data",response_data)
# 	for d in response_data["message"]:
# 			city_id = d["city_id"]
# 			if id:
# 				existing_doc = frappe.db.exists("Vendor City", {"city_id":city_id})
				
# 				if existing_doc:
# 					country = frappe.get_doc("Vendor City", existing_doc)
# 					# if country.country != d['name']:
# 					# 	print("country.country",d['name'],country.country)
						


# 				else:
# 					new_doc=frappe.new_doc("Vendor City")
# 					new_doc.city_id=d['city_id']
# 					new_doc.city=d['city']
# 					new_doc.state=d['state']
# 					new_doc.country=d['country']
# 					new_doc.insert(ignore_permissions=True)

# 	return response_data

@frappe.whitelist(allow_guest=True)
def get_city_list():
	city_list=frappe.db.sql("""select * from `tabVendor City` """,as_dict=1)
	return city_list

@frappe.whitelist()
def get_state(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""SELECT name ,state
	FROM `tabVendor State` 
	WHERE country_name = %(country_name)s
	
	 """.format(**{
				'key': searchfield
			}), {
			'txt': "%{}%".format(txt),
			'_txt': txt.replace("%", ""),
			'start': start,
			'page_len': page_len,
			'country_name':filters["country_name"]

		})
@frappe.whitelist()
def get_city(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""SELECT name ,city
	FROM `tabVendor City` 
	WHERE country = %(country)s and state=%(state)s
	
	 """.format(**{
				'key': searchfield
			}), {
			'txt': "%{}%".format(txt),
			'_txt': txt.replace("%", ""),
			'start': start,
			'page_len': page_len,
			'country':filters["country"],
			'state':filters["state"]

		})