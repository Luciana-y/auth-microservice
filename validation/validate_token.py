# validate_token.py
from utils import decode_token, token_table

def lambda_handler(event, context):
    headers = event.get("headers", {}) or {}
    auth = headers.get("Authorization") or headers.get("authorization")

    if not auth or not auth.startswith("Bearer "):
        return {"isAuthorized": False}

    token = auth.split(" ")[1]

    # verify JWT
    try:
        payload = decode_token(token)
    except:
        return {"isAuthorized": False}

    user_id = payload.get("sub")
    if not user_id:
        return {"isAuthorized": False}

    # check token table
    resp = token_table().get_item(Key={"user_id": user_id})
    item = resp.get("Item")
    if not item or item.get("token") != token:
        return {"isAuthorized": False}

    # authorized
    return {
        "isAuthorized": True,
        "context": {
            "userId": user_id,
            "type": payload.get("type"),
            "role": payload.get("role"),
            "tenant": payload.get("tenant"),
        }
    }