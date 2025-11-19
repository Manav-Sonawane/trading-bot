import hashlib
import time
from urllib.parse import urlencode
import hmac

def sign_params(params: dict, secret: str) -> dict:
    temp_params = params.copy()
    
    timestamp = int(time.time() * 1000)
    temp_params['timestamp'] = timestamp

    sorted_params = sorted(temp_params.items())

    query_string = urlencode(sorted_params)

    signature = hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    temp_params['signature'] = signature

    return temp_params

def mask_sensitive(params: dict) -> dict:
    masked = params.copy()
    if "signature" in masked:
        masked["signature"] = "***"
    return masked
