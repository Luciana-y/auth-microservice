#register_client.py
import json
import uuid
from datetime import datetime, timezone
from src.utils import (
    ok, error,
    find_cliente_by_email, cliente_table,
    hash_password
)

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        correo = (body.get("correo") or "").strip().lower()

        if not correo:
            return error("correo is required")
        if find_cliente_by_email(correo):
            return error("correo already exists", 409)

        password = body.get("contraseña")
        if not password or len(password) < 6:
            return error("contraseña must be >=6 chars")

        cliente_id = str(uuid.uuid4())
        item = {
            "cliente_id": cliente_id,
            "nombre": body.get("nombre", ""),
            "apellidos": body.get("apellidos", ""),
            "correo": correo,
            "numero": body.get("numero", ""),
            "documento": body.get("documento", ""),
            "fecha_nacimiento": body.get("fecha_nacimiento"),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "contraseña_hasheada": hash_password(password),
        }

        cliente_table().put_item(Item=item)
        del item["contraseña_hasheada"]

        return ok({"message": "cliente created", "cliente": item}, 201)

    except Exception as e:
        return error(str(e), 500)