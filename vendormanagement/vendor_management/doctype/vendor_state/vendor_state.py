# Copyright (c) 2023, Ideenkreice and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import json
import re

class VendorState(Document):
    def on_update(self):
        # self.set_state()
        frappe.enqueue(self.set_state)
    def on_trash(self):
        self.remove_state()
    def remove_state(self):
        base_url=get_api_settings()
        
        data={
			"name":self.name

		}
        url=base_url['base_url']+"/api/method/vendormanagement.vendor_management.doctype.vendor_state.vendor_state.get_state_remove"
        # url="http://localhost:8030/api/method/vendormanagement.vendor_management.doctype.vendor_details.vendor_details.get_vendor_list"
        response = requests.request("DELETE", url,headers = {
            'Content-Type': 'application/json',
            },json=data)
        response_data=response.json()
        print("Response:",response_data)
        return response_data

    def set_state(self):
        base_url=get_api_settings()
        if self.status=="unsync":

            url = base_url['base_url']+"/api/method/vendormanagement.vendor_management.doctype.vendor_state.vendor_state.update_state"
            data = {
            "name":self.name,
            "state":self.state,
            "state_code":self.state_code,
            "country_name": self.country_name
            }

            try:
                response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
                if response.status_code == 200:
                    print("State data updated on the external server.")
                else:
                    print("Failed to update state data on the external server. Status code:", response.status_code)
            except requests.exceptions.RequestException as e:
                    print("An error occurred during the request:", e)
@frappe.whitelist(allow_guest=True)
def update_state():
    
    data = frappe.form_dict
    try:
        # Check if a Vendor_Country document with the given ID already exists
        existing_doc = frappe.get_all("Vendor State", filters={"name": data.get("name")})

        if existing_doc:
            # Update the existing document with the new data
            existing_doc = frappe.get_doc("Vendor State", existing_doc[0].name)
            existing_doc.state = data.get("state")
            existing_doc.state_code = data.get("state_code")
            existing_doc.country_name = data.get("country_name")
            existing_doc.save(ignore_permissions=True)
        else:
            # Create a new Vendor_Country document and enter the data into it
            new_doc = frappe.new_doc("Vendor State")
            new_doc.state = data.get("state")
            new_doc.state_code = data.get("state_code")

            new_doc.country_name = data.get("country_name")
            new_doc.status="sync"

            new_doc.insert(ignore_permissions=True)

        return "state data updated or created successfully"
    except Exception as e:
        return "An error occurred while processing the request: " + str(e)

@frappe.whitelist(allow_guest=True)
def get_state_remove():
    data=frappe.form_dict
    frappe.delete_doc('Vendor State',data.name)
	
@frappe.whitelist(allow_guest=True)
def get_state_list():
	state_list=frappe.db.sql("""select * from `tabVendor State` """,as_dict=1)
	return state_list
@frappe.whitelist(allow_guest=True)
def get_state_filter(country_name):
	state_list=frappe.db.sql("""select * from `tabVendor State` where country_name=%(country_name)s """,values={'country_name':country_name},as_dict=1)
	return state_list
@frappe.whitelist(allow_guest=True)
def get_city_filter(country,state):
	print(country,state)
	city_list =frappe.db.sql("""select * from `tabVendor City` where country=%(country)s and state=%(state)s """,
	values={'country':country,'state':state},as_dict=1)
	return city_list
frappe.whitelist()
def get_api_settings():
	base_url=frappe.get_doc("Vendor API Settings").base_url
	api_key=frappe.get_doc("Vendor API Settings").api_key
	api_secret=frappe.get_doc("Vendor API Settings").api_secret
	return {'base_url':base_url,'api_key':api_key,'api_secret':api_secret}