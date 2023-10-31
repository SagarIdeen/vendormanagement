import frappe
from frappe import auth

@frappe.whitelist( allow_guest=True )
def login(usr, pwd):
    # Validating Login
    try:
        login_manager = frappe.auth.LoginManager()
        logged_user_email =frappe.db.get_all('User',
        or_filters=[
            ['email','=',usr],
            ['phone','=',usr],
            ['username','=',usr]
            ]
       )
        if(len(logged_user_email)==1):
            login_manager.authenticate(user=logged_user_email[0].name, pwd=pwd)
            login_manager.post_login()
        else:
            raise frappe.AuthenticationError()

    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        frappe.local.response["message"] = {
            "success_key":0,
            "message":"Authentication Error!"
        }

        return

    # Getting api key and secret
    api_generate = generate_keys(frappe.session.user)
    user = frappe.get_doc('User', frappe.session.user)

    frappe.response["message"] = {
        "success_key":1,
        "message":"Authentication success",
        "sid":frappe.session.sid,
        "api_key":user.api_key,
        "api_secret":api_generate,
        "username":user.username,
        "email":user.email
    }



def generate_keys(user):
    user_details = frappe.get_doc('User', user)
    api_secret = frappe.generate_hash(length=15)

    if not user_details.api_key:
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key
    

    user_details.api_secret = api_secret

    user_details.save(ignore_permissions=True)

    return api_secret