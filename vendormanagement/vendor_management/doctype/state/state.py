# Copyright (c) 2023, Ideenkreice and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class State(Document):
	pass

@frappe.whitelist(allow_guest=True)
def get_gst_code_for_state(state_name):
	print("gst",state_name)
	data=frappe.db.sql("""select gst_code from `tabState` where state=%(state)s """,values={'state':state_name},as_dict=1)
	print("gst",data)
	return data