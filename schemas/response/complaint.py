from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Enum

from schemas.base import BaseComplaint
from models.enums import State


class ComplaintOut(BaseComplaint):
    id: int
    photo_url: str
    created_at: datetime
    status: str # State