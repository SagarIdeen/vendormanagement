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
		
       
    };
});

