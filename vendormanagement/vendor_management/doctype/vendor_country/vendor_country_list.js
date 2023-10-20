frappe.listview_settings['Vendor_Country'] = {
    onload: function (listview) {
        // Add a custom button to the list view toolbar
        listview.page.add_button(__("GET COUNTRY"), function () {
            frappe.call({
                method: "vendormanagement.vendor_management.doctype.vendor_country.vendor_country.get_country()",
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
