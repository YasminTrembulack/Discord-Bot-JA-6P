from typing import Literal, Optional


from models.base import BaseResponse
from pydantic import BaseModel, Field


class EquipmentPayload(BaseModel):
    name: str = Field(..., description="Nome do equipamento")
    description: Optional[str] = Field(None, description="Descrição do equipamento")
    status: Literal['available', 'in_use', 'maintenance'] = Field(..., description="Status do equipamento",)


class EquipmentResponse(BaseResponse, EquipmentPayload):
    pass
