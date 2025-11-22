from utils import decode_token, token_table

def generate_policy(principal_id, effect, resource, context=None):
    auth_response = {
        "principalId": principal_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource
                }
            ]
        }
    }

    if context:
        auth_response["context"] = context

    return auth_response


def lambda_handler(event, context):
    headers = event.get("headers", {}) or {}
    auth = headers.get("Authorization") or headers.get("authorization")

    method_arn = event.get("methodArn")

    if not auth or not auth.startswith("Bearer "):
        return generate_policy("unknown", "Deny", method_arn)

    token = auth.split(" ")[1]

    try:
        payload = decode_token(token)
    except:
        return generate_policy("unknown", "Deny", method_arn)

    user_id = payload.get("sub")
    if not user_id:
        return generate_policy("unknown", "Deny", method_arn)

    # Verificar token en DynamoDB
    resp = token_table().get_item(Key={"user_id": user_id})
    item = resp.get("Item")
    if not item or item.get("token") != token:
        return generate_policy(user_id, "Deny", method_arn)

    # Success → Allow
    return generate_policy(
        user_id,
        "Allow",
        method_arn,
        {
            "userId": user_id,
            "type": payload.get("type"),
            "role": payload.get("role"),
            "tenant": payload.get("tenant"),
        }
    )
