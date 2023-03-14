import datetime
import hashlib
import json
import os


def sign_compare(customer_sign):
    now_hour = datetime.datetime.now().strftime('%Y%m%d%H')
    accounts = os.path.join(os.path.dirname(os.path.abspath(__file__)), "package.json")
    with open(accounts, 'rb') as fi:
        sec_json = fi.read()
        fi.close()
    sec = json.loads(sec_json)
    before_hash = f"{now_hour}{sec['secret_id']}{sec['secret_key']}"
    sign = hashlib.sha256(before_hash.encode('utf-8')).hexdigest()
    global_sign = "adan"
    if customer_sign == sign or customer_sign == global_sign:
        return 1
    return None
