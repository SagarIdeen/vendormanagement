// frappe.listview_settings['Vendor State'] = {
//     onload: function (listview) {
//         // Add a custom button to the list view toolbar
//         listview.page.add_button(__("GET STATE"), function () {
//             frappe.call({
//                 method: "vendormanagement.vendor_management.doctype.vendor_state.vendor_state.get_state",
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
