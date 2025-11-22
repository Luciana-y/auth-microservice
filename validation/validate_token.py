import json
from utils import decode_token, token_table

def lambda_handler(event, context):
    token = event.get("token")

    if not token:
        return {
            "statusCode": 403,
            "body": "Missing token"
        }

    # 1. Decodificar JWT
    try:
        payload = decode_token(token)
    except:
        return {
            "statusCode": 403,
            "body": "Invalid or expired JWT"
        }

    user_id = payload.get("sub")
    if not user_id:
        return {
            "statusCode": 403,
            "body": "Invalid token payload"
        }

    # 2. Validar token contra DynamoDB
    resp = token_table().get_item(Key={"user_id": user_id})
    item = resp.get("Item")

    if not item or item.get("token") != token:
        return {
            "statusCode": 403,
            "body": "Token revoked or not registered"
        }

    # 3. Si todo OK, retornar info del usuario para reglas de negocio
    return {
        "statusCode": 200,
        "body": json.dumps({
            "valid": True,
            "userId": user_id,
            "type": payload.get("type"),
            "role": payload.get("role"),
            "tenant": payload.get("tenant")
        })
    }
