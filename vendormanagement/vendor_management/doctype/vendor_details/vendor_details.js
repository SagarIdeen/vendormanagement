// Copyright (c) 2023, Ideenkreice and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vendor Details', {
	
	refresh: function (frm) {
		console.log(frm.doc.status);
		if (frm.doc.status == "New") {
			frm.events.approve_reject(frm)
		} else {
			frm.page.clear_actions_menu();
			frm.disable_save()
		}

		frm.events.show_duplication(frm)

	},
	on_submit: function (frm) {
		console.log('test after save');
	},
	approve_reject: function (frm) {
		frm.page.add_action_item("Approve", () => {
			frm.doc.status = "Approved";
			frm.dirty();
			frm.save();
		});

		frm.page.add_action_item("Reject", () => {
			frm.doc.status = "Rejected";
			frm.dirty();
			frm.save();
		});
	},
	show_duplication: function (frm) {
		if(frm.doc.pan_number || frm.doc.din || frm.doc.mobile_number)
		{
			frappe.call({
				method:
					"vendormanagement.vendor_management.doctype.vendor_details.vendor_details.duplicate",
				args: {
					name: frm.docname,
					pan_number: frm.doc.pan_number,
					din: frm.doc.din,
					mobile: frm.doc.mobile_number
	
				},
				freeze: true,
				callback: (r) => {
					if (r.message?.length == 0) {
						frm.set_df_property("duplicate", "hidden", 1);
					}
					else {
						frm.set_df_property("duplicate", "hidden", 0);
						$(
							frappe.render_template("duplicate", {
								data: r.message
							})
						).appendTo(frm.fields_dict.duplicate.$wrapper.empty());
					}
				},
				error: (r) => {
					frappe.msgprint(r);
				},
			});

		}
		


	},
	
	 
});