from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    member_id: str
    username: str
    full_name: str
    created_at: datetime
