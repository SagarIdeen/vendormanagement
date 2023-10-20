// frappe.listview_settings['Vendor City'] = {
//     onload: function (listview) {
//         // Add a custom button to the list view toolbar
//         listview.page.add_button(__("Sync"), function () {
//             frappe.call({
//                 method: "vendormanagement.vendor_management.doctype.vendor_city.vendor_city.get_city",
//                 freeze: true,
//                 callback: function (r) {
//                     console.log(r.message);
                   
                    
//                 },
//                 error: function (r) {
//                     frappe.msgprint(r.message);
//                 },
//             });
//         });
//     }
// };
