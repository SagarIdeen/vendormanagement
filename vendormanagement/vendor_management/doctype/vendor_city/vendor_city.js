// Copyright (c) 2023, Ideenkreice and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vendor City', {
	// refresh: function(frm) {

	// }
	country:function(frm){
		frm.set_query('state', function () {
			return {
				query: "vendormanagement.vendor_management.doctype.vendor_city.vendor_city.get_state",
				filters: { 'country_name': frm.doc.country }
			};
		});
	}
});
