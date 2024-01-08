// Copyright (c) 2023, Ideenkreice and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vendor Details', {
	
	refresh: function (frm) {
		if (frm.doc.status == "New") {
			frm.events.approve_reject(frm)
		} else {
			frm.page.clear_actions_menu();
			frm.disable_save()
		}

		frm.events.show_duplication(frm)

	},
	preview:function(frm){
		window.open(frm.doc.attachements);
		// frm.call({
		// 	method:"get_image",
		// 	args:{
		// 		name:frm.docname
		// 	}
		// }

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
	country:function(frm){
		
		frm.trigger('get_state')
		frm.trigger('get_city')
	},
	state:function(frm){
		frm.trigger('get_city')
	},
	get_state(frm){
		frm.set_query('state', function () {
			return {
				query: "vendormanagement.vendor_management.doctype.vendor_city.vendor_city.get_state",
				filters: { 'country_name': frm.doc.country }
			};
		});

	},
	get_city(frm){
		if ((frm.doc.country)&&(frm.doc.state)){
			frm.set_query('city', function () {
				return {
					query: "vendormanagement.vendor_management.doctype.vendor_city.vendor_city.get_city",
					filters: { 'country': frm.doc.country,'state':frm.doc.state }
				};
			});

		}
		

	}

	
	 
});
