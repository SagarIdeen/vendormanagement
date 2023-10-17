# Copyright (c) 2023, Ideenkreice and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.share import add as add_share
import requests
import json

class VendorDetails(Document):
	



	def on_update(self):
		get_vendor_data()
		get_vendor_list()
		# vendor_data=frappe.db.sql("""select name,din,mobile_number,pan_number from `tabVendor  details` where name !=%(name)s and ( din=%(din)s or pan_number=%(pan_number)s 
		# or mobile_number=%(mobile_number)s)""",values={'din':self.din,'pan_number':self.pan_number,'mobile_number':self.mobile_number,'name':self.name},as_dict=1)
		# if vendor_data:
		# 	self.reference=[]
		# 	for d in vendor_data:
		# 		description=[]
		# 		if d.din==self.din:
		# 			description.append("Din Number")
		# 		if d.pan_number==self.pan_number:
		# 			description.append("Pan Number")
		# 		if d.mobile_number==self.mobile_number:
		# 			description.append("Mobile Number")
		# 		description_str = ', '.join(description)+" Duplicated"
				
		# 		self.append('reference',{
		# 			'reference':d['name'],
		# 			'description':description_str 
				# })
				# pass
			
	
	def before_insert(self):
		# vendor_data=frappe.db.sql("""select name,din,mobile_number,pan_number from `tabVendor  details` where  din=%(din)s or pan_number=%(pan_number)s 
		# or mobile_number=%(mobile_number)s""",values={'din':self.din,'pan_number':self.pan_number,'mobile_number':self.mobile_number,'name':self.name},as_dict=1)
		# print("vendor data",vendor_data)
		# if vendor_data:
		# 	self.reference=[]
		# 	for d in vendor_data:
		# 		description=[]
		# 		if d.din==self.din:
		# 			description.append("Din Number")
		# 		if d.pan_number==self.pan_number:
		# 			description.append("Pan Number")
		# 		if d.mobile_number==self.mobile_number:
		# 			description.append("Mobile Number")
		# 		description_str = ', '.join(description)+" Duplicated"
				
		# 		self.append('reference',{
		# 			'reference':d['name'],
		# 			'description':description_str 
		# 		})
		pass
			
@frappe.whitelist()
def duplicate(name,pan_number,din,mobile):
	vendor_data=frappe.db.sql("""select name,din,mobile_number,pan_number,status from `tabVendor Details` where name !=%(name)s and ( din=%(din)s or pan_number=%(pan_number)s 
		or mobile_number=%(mobile_number)s)""",values={'din':din,'pan_number':pan_number,'mobile_number':mobile,'name':name},as_dict=1)
	

	for d in vendor_data:
		description=[]
		if d.din==din:
			description.append("Din Number")
		if d.pan_number==pan_number:
			description.append("Pan Number")
		if d.mobile_number==mobile:
			description.append("Mobile Number")
		description_str = ', '.join(description)+" Duplicated"
		
		d['description'] = description_str
	return vendor_data


@frappe.whitelist()
def get_vendor_data():
	url="http://localhost:8030/api/method/vendormanagement.vendor_management.doctype.vendor_details.vendor_details.get_vendor_list"
	response = requests.request("GET", url,headers = {
			'Content-Type': 'application/json',
				})
	response_data=response.json()
	
	print("Response:",response_data)
@frappe.whitelist(allow_guest=True)
def get_vendor_list():
	# data=frappe.get_all("Vendor Details",filters={}, fields=['name'])
	data=frappe.db.sql("""select * from `tabVendor Details` """,as_dict=1)
	return data
	
			
		

			