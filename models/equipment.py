from typing import Literal

from models.base import BaseResponse
from pydantic import BaseModel, Field


class EquipmentPayload(BaseModel):
    name: str = Field(..., description="Nome do equipamento")
    description: str = Field(..., description="Descrição do equipamento")
    status: Literal['available', 'in_use', 'maintenance'] = Field(..., description="Status do equipamento",)


class EquipmentResponse(BaseResponse, EquipmentPayload):
    pass
