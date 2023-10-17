frappe.listview_settings['Vendor Details'] = {
    onload: function (listview) {
        // Add a custom button to the list view toolbar
        listview.page.add_button(__("Sync"), function () {
            frappe.call({
                method: "vendormanagement.vendor_management.doctype.vendor_details.vendor_details.get_vendor_data",
                freeze: true,
                callback: function (r) {
                    console.log(r.message);
                   
                    
                },
                error: function (r) {
                    frappe.msgprint(r.message);
                },
            });
        });
    }
};
