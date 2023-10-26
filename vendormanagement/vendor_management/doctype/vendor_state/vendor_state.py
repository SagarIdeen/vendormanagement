# Copyright (c) 2023, Ideenkreice and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import json
import re

class VendorState(Document):
	pass
@frappe.whitelist(allow_guest=True)
def get_state():
	url="http://35.154.0.123:8080/api/method/vendormanagement.vendor_management.doctype.vendor_country.vendor_country.get_state_list"
	response = requests.request("GET", url,headers = {
			'Content-Type': 'application/json',
				})
	response_data=response.json()
	for d in response_data["message"]:
			state_id  = d["state_id"]
			if id:
				existing_doc = frappe.db.exists("Vendor State", {"state_id":state_id })
				
				if existing_doc:
					country = frappe.get_doc("Vendor State", existing_doc)
					# if country.country != d['name']:
					# 	print("country.country",d['name'],country.country)
						


				else:
					new_doc=frappe.new_doc("Vendor State")
					new_doc.state_id =d['state_id']
					new_doc.state =d['state']
					new_doc.state_code=d['state_code']
					new_doc.country_name=d['country_name']
					new_doc.insert(ignore_permissions=True)

	return response_data

@frappe.whitelist(allow_guest=True)
def get_state_list():
	state_list=frappe.db.sql("""select * from `tabVendor State` """,as_dict=1)
	return state_list
@frappe.whitelist(allow_guest=True)
def get_state_filter(country_name):
	state_list=frappe.db.sql("""select * from `tabVendor State` where country_name=%(country_name)s """,values={'country_name':country_name},as_dict=1)
	return state_list
@frappe.whitelist()
def get_city_filter(country,state):
	print(country,state)
	city_list =frappe.db.sql("""select * from `tabVendor City` where country=%(country)s and state=%(state)s """,
	values={'country':country,'state':state},as_dict=1)
	return city_list