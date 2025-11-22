import boto3
import json
from utils import ok, error

def invoke_token_validator(token):
    lambda_client = boto3.client("lambda")

    payload = json.dumps({"token": token})

    response = lambda_client.invoke(
        FunctionName="auth-microservice-dev-validateToken",
        InvocationType="RequestResponse",
        Payload=payload
    )

    return json.loads(response["Payload"].read())


def lambda_handler(event, context):
    headers = event.get("headers", {}) or {}
    auth = headers.get("Authorization") or headers.get("authorization")

    if not auth:
        return error("Missing Authorization header", 401)

    # 🔓 Se permite token sin Bearer
    token = auth.replace("Bearer ", "").strip()

    # 🔒 Validar token llamando al lambda de seguridad
    validation = invoke_token_validator(token)

    if validation.get("statusCode") != 200:
        return error("Forbidden - Acceso No Autorizado", 403)

    user = json.loads(validation["body"])

    # 🧠 Validar reglas de negocio
    if user.get("type") != "worker":
        return error("only workers allowed", 403)

    if user.get("role") != "admin":
        return error("admin role required", 403)

    return ok({
        "message": "welcome admin!",
        "userId": user.get("userId"),
        "role": user.get("role")
    })
