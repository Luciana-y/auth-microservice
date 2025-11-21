# register_worker.py
import json
import uuid
from src.utils import (
    ok, error,
    find_trabajador_by_email, trabajador_table,
    hash_password
)

ALLOWED_ROLES = {"admin", "cocina", "delivery"}

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        correo = (body.get("correo") or "").strip().lower()
        role = body.get("rol")

        if role not in ALLOWED_ROLES:
            return error("invalid role")
        if find_trabajador_by_email(correo):
            return error("correo already exists", 409)

        password = body.get("contraseña")
        if not password or len(password) < 6:
            return error("contraseña must be >=6 chars")

        trabajador_id = str(uuid.uuid4())
        item = {
            "trabajador_id": trabajador_id,
            "tenant_id": body.get("tenant_id"),
            "nombre": body.get("nombre", ""),
            "apellidos": body.get("apellidos", ""),
            "correo": correo,
            "documento": body.get("documento", ""),
            "numero_telefono": body.get("numero_telefono", ""),
            "rol": role,
            "contraseña_hasheada": hash_password(password),
        }

        trabajador_table().put_item(Item=item)
        del item["contraseña_hasheada"]

        return ok({"message": "trabajador created", "trabajador": item}, 201)

    except Exception as e:
        return error(str(e), 500)