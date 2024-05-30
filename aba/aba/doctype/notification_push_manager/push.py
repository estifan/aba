import frappe
from pywebpush import webpush, WebPushException

@frappe.whitelist()
def push(endpoint='',p256dh='',auth='',user='',data=''):
    try:
        webpush(
            subscription_info={
                "endpoint": endpoint,
                "keys": {
                    "p256dh": p256dh,
                    "auth": auth
                }},
            data=data,
            vapid_private_key="CZtf_JUxmXkCKbzwaKedPPO9BFC99U2rk-GUYDbYAa8",
            vapid_claims={
                    "sub": f"mailto:{user}",
                }
        )
        return "done."
    except WebPushException as ex:
        print("error: {}", repr(ex))
        return "Error."
    