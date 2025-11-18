from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BaseResponse(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    # deleted_at: Optional[datetime]
