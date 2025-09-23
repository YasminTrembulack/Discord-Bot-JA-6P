from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    username: str
    global_name: str | None = None
    joined_at: datetime
