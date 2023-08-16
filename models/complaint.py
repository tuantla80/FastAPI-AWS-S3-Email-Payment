import sqlalchemy
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, Enum, ForeignKey

from db import metadata
from models.enums import State

complaint = sqlalchemy.Table(
    "complaints",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(120), nullable=False),
    Column("description", Text, nullable=False),
    Column("pho to_url", String(200), nullable=False),
    Column("amount", Float, nullable=False),
    Column("created_at", DateTime, server_default=sqlalchemy.func.now()),
    Column("status", Enum(State), nullable=False, server_default=State.pending.name),
    Column("complainer_id", ForeignKey("users.id"), nullable=False),
)
