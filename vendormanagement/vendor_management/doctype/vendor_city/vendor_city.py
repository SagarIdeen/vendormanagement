# Copyright (c) 2023, Ideenkreice and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class VendorCity(Document):
	pass
@frappe.whitelist()
def get_city():
	city=frappe.db.sql("""select * from `tabvendor_demo_city` """,as_dict=1)
	for d in city:
		state=d['state']+'-'+d['state_id']
		
		new_doc=frappe.new_doc("Vendor City")
		new_doc.city=d['city']
		new_doc.city_id=d['city_id']
		new_doc.state=state
		new_doc.state_id=d['state_id']
		new_doc.state_code=d['state_code']
		new_doc.country_id=d['country_id']
		new_doc.country =d['country']
		new_doc.country_code=d['country_code']
		

		new_doc.insert(ignore_permissions=True)
	return city