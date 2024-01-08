# Copyright (c) 2023, Ideenkreice and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.share import add as add_share
import requests
import json
import re
import os
from frappe.utils.file_manager import save_url
from frappe.utils.background_jobs import enqueue


class VendorDetails(Document):
	pass
@frappe.whitelist(allow_guest=True)
def get_image(name):
	attachment=frappe.get_doc("Vendor Details",name)
	return attachment.attachements

				
@frappe.whitelist()
def duplicate(name,pan_number,din,mobile):
	vendor_data=frappe.db.sql("""select name,din,mobile_number,pan_number,status from `tabVendor Details` where name !=%(name)s and
	 ( (din = %(din)s AND din != '')
            OR (pan_number = %(pan_number)s AND pan_number != '')
            OR (mobile_number = %(mobile_number)s AND mobile_number != ''))""",values={'din':din,'pan_number':pan_number,'mobile_number':mobile,'name':name},as_dict=1)
	

	for d in vendor_data:
		
		description=[]
		if d.din is not '':
			

			if d.din==din:
				description.append("Din Number")
		if d.pan_number is not '':

			if d.pan_number==pan_number:
				description.append("Pan Number")
		if d.mobile_number==mobile:
			description.append("Mobile Number")
		if description:
			description_str = ', '.join(description)+" Duplicated"
			d['description'] = description_str
	return vendor_data


@frappe.whitelist(allow_guest=True)
def get_vendor_list():
	
	data=frappe.db.sql("""select * from `tabVendor Details` """,as_dict=1)
	print("data",data)
	return data

@frappe.whitelist(allow_guest=True)
def get_vendor_data():
	
	data=get_api_settings()
	
	
	url=data['base_url']+"/api/method/vendormanagement.vendor_management.doctype.vendor_details.vendor_details.get_vendor_list"
	# url="http://localhost:8030/api/method/vendormanagement.vendor_management.doctype.vendor_details.vendor_details.get_vendor_list"
	response = requests.request("GET", url,headers = {
			'Content-Type': 'application/json',
				})
	response_data=response.json()
	print("Response:",response_data)
	# enqueue_receive_and_create_vendor_data(response_data)
	receive_and_create_vendor_data(response_data)
	# return response_data

@frappe.whitelist(allow_guest=True)	
def enqueue_receive_and_create_vendor_data(response_data):
    frappe.enqueue(
       receive_and_create_vendor_data,
        data=response_data,
         
    )
	

@frappe.whitelist(allow_guest=True)
def receive_and_create_vendor_data(data):
		api_data=get_api_settings()
		api_key=api_data['api_key']
		api_secret=api_data['api_secret']
		print("apis",api_key,api_secret)
	# Deserialize the received data
		received_data = data
		print("received_data",received_data)

		for d in received_data["message"]:
			name = d["name"]
			if name:
				existing_doc = frappe.db.exists("Vendor Details", {"name1": name})
				if existing_doc:
					print(" if Document with name {} already exists.".format(name))

				else:
					new_doc=frappe.new_doc("Vendor Details")
					print("else Document with name {} already exists.".format(name))
					new_doc.name1=name
					new_doc.address1=d['address1']
					new_doc.address_2=d['address_2']
					new_doc.bank_branch=d['bank_branch']
					new_doc.bank_name=d['bank_name']
					new_doc.attachements=d['attachements']
					new_doc.country=d['country']
					new_doc.city=d['city']
					new_doc.contact_person_1=d['contact_person_1']
					new_doc.contact_person_2=d['contact_person_2']
					new_doc.din=d['din']
					new_doc.gst_provisional_id=d['gst_provisional_id']
					new_doc.ifsc_code=d['ifsc_code']
					new_doc.mobile_number=d['mobile_number']
					new_doc.msme_category=d['msme_category']
					new_doc.pan_number=d['pan_number']
					new_doc.pin_code=d['pin_code']
					new_doc.state=d['state']
					new_doc.status=d['status']
					new_doc.street=d['street']
					new_doc.telephone_number=d['telephone_number']
					new_doc.vendor_name=d['vendor_name']
					new_doc.banking_account_number=d['banking_account_number']

					new_doc.insert(ignore_permissions=True)
					

					# url = "http://localhost:8030/api/method/upload_file"
					
					if d['attachements']:
						# regex= 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
						# checkURL= re.findall(regex,d['attachements'])
						# print("checkURL",checkURL)
						# if checkURL:
						# 	remote_file_url=d['attachements']
						# else:

						headers = {
						'Authorization': 'token '+api_key+':'+api_secret					}


					
						remote_file_url=api_data['base_url']+d['attachements']
						# remote_file_response = requests.get(remote_file_url)
						remote_file_response = requests.request("GET", remote_file_url, headers=headers)

						print("remote_file_response",remote_file_response)
						
						frappe.get_doc(
						{
							"doctype": "File",
							"attached_to_doctype":'Vendor Details',
							"attached_to_name": new_doc.name,
							"attached_to_field": 'attachements',
							"folder": 'Home',
							"file_name": remote_file_url.split('/')[-1],
							# "file_url": remote_file_url,
							"file_url": d['attachements'],
							"is_private": 1,
							"content": remote_file_response.content,
						}
						).save(ignore_permissions=True)

		return "Data received and processed successfully."
frappe.whitelist()
def get_api_settings():
	base_url=frappe.get_doc("Vendor API Settings").base_url
	api_key=frappe.get_doc("Vendor API Settings").api_key
	api_secret=frappe.get_doc("Vendor API Settings").api_secret
	return {'base_url':base_url,'api_key':api_key,'api_secret':api_secret}


