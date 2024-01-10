frappe.ready(function () {
  console.log("webform");
  frappe.web_form.validate = () => {
    let data = frappe.web_form.get_values();
  
    const pan_number = data.pan_number;
    const gst_number = data.gst_provisional_id;
    const stateName = data.state;
    const country = data.country;
    let phone = data.mobile_number;
    // if (phone == undefined) {
    //   frappe.msgprint("Phone Number Is Mandatory");
    //   return false;
    // }
    // if (country == undefined) {
    //   frappe.msgprint("Country Is Mandatory");
    //   return false;
    // }

    if (country === "India") {
      // PAN Number Validation
      if (!pan_number) {
        frappe.msgprint(__("PAN Number is mandatory for India."));
        return false; // Prevent form submission
      } else {
        const panNumberPattern = /^[A-Z]{5}[0-9]{4}[A-Z]$/;
        if (!panNumberPattern.test(pan_number)) {
          frappe.msgprint(
            __("Invalid PAN Number. Please enter a valid PAN Number.")
          );
          return false; // Prevent form submission
        }
      }

      // GST Validation
      if (!gst_number) {
        frappe.msgprint(__("GST Number is mandatory for India."));
        return false; // Prevent form submission
      } else {
        // Define a regular expression pattern for GST code validation in India
        const gstCodePattern =
          /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][0-9]{1}[Z][0-9]{1}$/;
        if (!gstCodePattern.test(gst_number)) {
          frappe.msgprint(
            __("Invalid GST Number. Please enter a valid GST Number.")
          );
          return false;
        }
      }
    }

    return true; // Allow form submission for non-India countries
    }

  
    
    
  // filters
  frappe.web_form.on("country", (field, value) => {
    update_state_filters();
    update_city_filters();
  });

  frappe.web_form.on("state", (field, value) => {
    update_city_filters();
  });

  function update_state_filters() {
    const country_name = frappe.web_form.get_value("country");

    if (country_name) {
      // let  myurl='api/resource/State';
      $.ajax({
        method: "GET",

        url: `/api/method/vendormanagement.vendor_management.doctype.vendor_state.vendor_state.get_state_filter?country_name=${country_name}`,
        // url:myurl,
        success: function (result) {
          const options = result.message.map((state) => {
            return {
              label: state.state,
              value: state.name,
            };
          });

          console.log("options", options);

          const stateField = frappe.web_form.get_field("state");
          stateField._data = options;
          stateField.refresh();
        },
      });
    }
  }
  function update_city_filters() {
    let country = frappe.web_form.get_value("country");
    let state = frappe.web_form.get_value("state");

    if (country && state) {
      // let  myurl='api/resource/State';
      $.ajax({
        method: "GET",

        url: `/api/method/vendormanagement.vendor_management.doctype.vendor_state.vendor_state.get_city_filter?country=${country}&state=${state}`,
        // url:myurl,
        success: function (result) {
          const options = result.message.map((city) => {
            return {
              label: city.city,
              value: city.name,
            };
          });

          console.log("options", options);

          const cityField = frappe.web_form.get_field("city");
          cityField._data = options;
          cityField.refresh();
        },
      });
    }
  }
});
