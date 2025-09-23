from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    member_id: int
    username: str
    full_name: str
    created_at: datetime
