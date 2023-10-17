frappe.ready(function() {
    // Bind events here
    frappe.web_form.validate = () => {
        let data = frappe.web_form.get_values();
		// Validation for Pan Number
        let pan_number = data.pan_number;
		if (pan_number){
			 // Replace the pattern with the correct format for PAN numbers
			 let panNumberPattern = /^[A-Z]{5}[0-9]{4}[A-Z]$/;

			 // Check if the entered PAN number matches the pattern
			 if (!panNumberPattern.test(pan_number)) {
				 frappe.msgprint(__("Invalid PAN Number. Please enter a valid PAN Number."));
				 return false; 
			 }
			 return true;

		}

		// GST Validation
		let gst_number = data.gst_number;
		const stateName = data.state; // Assuming state is a field on your web form
        const gstCode =  getGSTCodeForState(stateName);
		if(gst_number && pan_number){
			let gst_pan_portion = gst_number.substr(2, 5);
			// Check if the extracted GST PAN portion matches the entered PAN number
            if (gst_pan_portion !== pan_number) {
                frappe.msgprint(__("The PAN number does not match the GST number. Please enter a matching PAN number."));
                return false; 
            }
			// Replace the pattern with the correct format for GST numbers
			let gstNumberPattern = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9]{1}$/;

			if (!gstNumberPattern.test(gst_number)) {
				frappe.msgprint(__("Invalid GST Number. Please enter a valid GST Number."));
				return false; 
			}
	
			
			return true;

		}
		if(gst_number && pan_number){
			let gst_pan_portion = gst_number.substr(2, 5);
			// Check if the extracted GST PAN portion matches the entered PAN number
            if (gst_pan_portion !== pan_number) {
                frappe.msgprint(__("The PAN number does not match the GST number. Please enter a matching PAN number."));
                return false; 
            }
			// Replace the pattern with the correct format for GST numbers
			let gstNumberPattern = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9]{1}$/;

			if (!gstNumberPattern.test(gst_number)) {
				frappe.msgprint(__("Invalid GST Number. Please enter a valid GST Number."));
				return false; 
			}
	
			
			return true;

		}

        
		
       
    };
	async function getGSTCodeForState(stateName) {
		try {
			const response = await frappe.call({
				method: "vendormanagement.vendor_management.doctype.state.state.get_gst_code_for_state",
				args: { state_name: stateName },
			});
	
			if (response.message) {
				return response.message;
			} else {
				return null;
			}
		} catch (error) {
			frappe.msgprint(__("An error occurred while fetching the GST code."));
			return null;
		}
	}
		
	
});


