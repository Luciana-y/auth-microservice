# utils.py
import os
import json
import time
import uuid
import boto3
import bcrypt
import jwt
from datetime import datetime, timezone
from boto3.dynamodb.conditions import Key

# ------------------------
# ENV
# ------------------------
DYNAMO_CLIENTE_TABLE = os.environ.get("DYNAMO_CLIENTE_TABLE")
DYNAMO_TRABAJADOR_TABLE = os.environ.get("DYNAMO_TRABAJADOR_TABLE")
DYNAMO_TOKEN_TABLE = os.environ.get("DYNAMO_TOKEN_TABLE")

JWT_SECRET = os.environ.get("JWT_SECRET", "default-secret")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
JWT_EXP_SECONDS = int(os.environ.get("JWT_EXP_SECONDS", "3600"))

ddb = boto3.resource("dynamodb")


# -------------------------------
# RESPONSE HELPERS
# -------------------------------
def ok(body, status=200):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def error(msg, status=400):
    return ok({"error": msg}, status)


# -------------------------------
# DYNAMODB HELPERS
# -------------------------------
def cliente_table():
    return ddb.Table(DYNAMO_CLIENTE_TABLE)


def trabajador_table():
    return ddb.Table(DYNAMO_TRABAJADOR_TABLE)


def token_table():
    return ddb.Table(DYNAMO_TOKEN_TABLE)


def find_cliente_by_email(email: str):
    resp = cliente_table().query(
        IndexName="correo-index",
        KeyConditionExpression=Key("correo").eq(email),
    )
    return resp["Items"][0] if resp["Items"] else None


def find_trabajador_by_email(email: str):
    resp = trabajador_table().query(
        IndexName="correo-index",
        KeyConditionExpression=Key("correo").eq(email),
    )
    return resp["Items"][0] if resp["Items"] else None


# -------------------------------
# PASSWORD HANDLING
# -------------------------------
def hash_password(password: str) -> str:
    pwd = password.encode("utf-8")
    hashed = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hashed.decode("utf-8")


def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


# -------------------------------
# JWT HANDLING
# -------------------------------
def generate_token(payload: dict) -> str:
    now = int(time.time())
    data = payload.copy()
    data["iat"] = now
    data["exp"] = now + JWT_EXP_SECONDS
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])