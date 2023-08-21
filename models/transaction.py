from sqlalchemy import Table, Column, Integer, Float, String, ForeignKey

from db import metadata


transaction = Table(
   'transactions',
   metadata,
   Column("id", Integer, primary_key=True),
   Column("quote_id", String(120), nullable=False),
   Column("transfer_id", Integer, nullable=False),
   Column("target_account_id", String(100), nullable=False),
   Column("amount", Float),
   Column("complaint_id", ForeignKey("complaints.id")),
)
