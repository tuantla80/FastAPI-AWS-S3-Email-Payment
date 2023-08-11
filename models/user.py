import sqlalchemy
from sqlalchemy import Column, Integer, String, Enum

from db import metadata
from models.enums import RoleType

user = sqlalchemy.Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(120), unique=True),
    Column("password", String(255)),
    Column("first_name", String(200)),
    Column("last_name", String(200)),
    Column("phone_name", String(20)),
    Column("role", Enum(RoleType), nullable=False, server_default=RoleType.complainer.name),
    Column("iban", String(200)),
)
