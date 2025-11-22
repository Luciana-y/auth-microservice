# admin_only.py
from utils import ok, error

def lambda_handler(event, context):
    auth = event.get("requestContext", {}).get("authorizer", {})

    if auth.get("type") != "worker":
        return error("only workers allowed", 403)

    if auth.get("role") != "admin":
        return error("admin role required", 403)

    return ok({"message": "welcome admin!", "userId": auth.get("userId")})