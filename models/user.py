from datetime import datetime
from typing import List, Optional

from models.base import BaseResponse
from pydantic import BaseModel, Field


class UserPayload(BaseModel):
    username: str = Field(..., description="Nome global do usuário")
    member_id: Optional[str] = Field(None, description="ID do usuário (Discord)")
    full_name: Optional[str] = Field(None, description="Nome completo ou de exibição do usuário")
    email: Optional[str] = Field(None, description="Email do usuário")
    created_at: datetime = Field(default_factory=datetime.now, description="Data de criação do registro")
    roles: Optional[List[str]] = Field(default_factory=list, description="Lista de cargos/roles do usuário")

 
class UserResponse(BaseResponse, UserPayload):
    pass
