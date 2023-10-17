frappe.ready(function () {
  frappe.web_form.validate = () => {
    const data = frappe.web_form.get_values();
    const pan_number = data.pan_number;
    const gst_number = data.gst_provisional_id;
    const stateName = data.state;

    // PAN Number Validation
    if (pan_number) {
      const panNumberPattern = /^[A-Z]{5}[0-9]{4}[A-Z]$/;
      if (!panNumberPattern.test(pan_number)) {
        frappe.msgprint(
          __("Invalid PAN Number. Please enter a valid PAN Number.")
        );
        return false; // Prevent form submission
      }
    }

    // GST Validation
    if (gst_number) {
      // Define a regular expression pattern for GST code validation in India
      const gstCodePattern =
        /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][0-9]{1}[Z][0-9]{1}$/;
      if (!gstCodePattern.test(gst_number)) {
        frappe.msgprint(
          __("Invalid GST Number. Please enter a valid GST Number.")
        );
        return false;
      }
      return true;
    }
  };
});

//     let gstCodes = await getGSTCodeForState(stateName);
// 	console.log("gst_code",gstCodes);
//     if (gstCodes) {

//         let gstCodePortion = gst_number.substr(0, 2); // Extract first 2 characters as GST code
// 		 let panPortion = gst_number.substr(2, 10); // Extract next 10 characters as PAN number
// 		let gstNumberPattern = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9]$/;

//         if (gstCodePortion !== gstCodes || panPortion !== pan_number || !gstNumberPattern.test(gst_number)) {
// 			console.log("gst_code1",gstCodes);
//             frappe.msgprint(__("Invalid GST Number. Please enter a valid GST Number."));
//             return false;
//         }
//     } else {
//         frappe.msgprint(__("No GST code found for the selected state."));
//         return false;
//     }

function getGSTCodeForState(stateName) {
  return new Promise((resolve, reject) => {
    frappe.call({
      method:
        "vendormanagement.vendor_management.doctype.state.state.get_gst_code_for_state",
      args: {
        state_name: stateName,
      },
      freeze: true,
      callback: (r) => {
        if (r.message && r.message[0] && r.message[0].gst_code) {
          resolve(r.message[0].gst_code);
        } else {
          resolve(null);
        }
      },
      error: (r) => {
        reject(r);
      },
    });
  });
}
