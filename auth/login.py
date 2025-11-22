# login.py
import json
from datetime import datetime, timezone
from utils import (
    ok, error,
    find_trabajador_by_email, find_cliente_by_email,
    token_table,
    generate_token, check_password
)

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        correo = (body.get("correo") or "").strip().lower()
        password = body.get("contraseña")

        if not correo or not password:
            return error("correo & contraseña required")

        # Try worker
        worker = find_trabajador_by_email(correo)
        if worker:
            if not check_password(password, worker["contraseña_hasheada"]):
                return error("invalid credentials", 401)

            payload = {
                "sub": worker["trabajador_id"],
                "type": "worker",
                "role": worker["rol"],
                "tenant": worker["tenant_id"],
            }

            token = generate_token(payload)
            token_table().put_item(Item={
                "user_id": worker["trabajador_id"],
                "token": token,
                "type": "worker",
                "created_at": datetime.now(timezone.utc).isoformat()
            })
            return ok({"token": token, "type": "worker"})

        # Try client
        client = find_cliente_by_email(correo)
        if client:
            if not check_password(password, client["contraseña_hasheada"]):
                return error("invalid credentials", 401)

            payload = {
                "sub": client["cliente_id"],
                "type": "user",
                "role": None,
            }

            token = generate_token(payload)
            token_table().put_item(Item={
                "user_id": client["cliente_id"],
                "token": token,
                "type": "user",
                "created_at": datetime.now(timezone.utc).isoformat()
            })
            return ok({"token": token, "type": "user"})

        return error("user not found", 404)

    except Exception as e:
        return error(str(e), 500)