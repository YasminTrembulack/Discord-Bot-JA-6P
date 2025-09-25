from asyncio import Lock
from datetime import time, datetime
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class UserReservationState:
    def __init__(self):
        self.lock = Lock()
        self.equipment_name = None
        self.equipment_id = None
        self.date = None
        self.start_time = None
        self.end_time = None
        self.unavailable_times = []
        self.reservation_id = None


class BaseResponse(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

class UserPayload(BaseModel):
    member_id: str
    username: str
    full_name: str
    created_at: datetime
    
class UserResponse(BaseResponse, UserPayload):
    pass

class EquipmentPayload(BaseModel):
    name: str
    description: str
    status: Literal['available', 'in_use', 'maintenance']

class EquipmentResponse(BaseResponse, EquipmentPayload):
    pass

class ReservationConfig(BaseModel):
    id: int = Field(default=1, description="Identificador único da configuração")
    start_time: time = Field(..., description="Horário de início do funcionamento")
    end_time: time = Field(..., description="Horário de término do funcionamento")
    reservation_chanel: Optional[str] = Field(default=None, description="Nome do canal onde o bot vai ver a reservas, caso None lê todo os canais")
    reservation_approval_chanel: Optional[str] = Field(default=None, description="Nome do canal onde o bot vai mandas as reservas para aprovação, caso None ele entende que não precisa de aprovação")
    max_reservation_blocks: int = Field(..., description="Quantos blocos de min_reservation podem ser encaixados em uma reserva (ex: 3).")
    min_reservation: int = Field(..., gt=0, description="Tempo mínimo de cada reserva em minutos")
    max_reservation_days: int = Field(..., gt=0, description="Quantos dias no futuro é possível reservar")
    days_of_week: List[int] = Field(default_factory=lambda: [1,2,3,4,5],
                                    description="Dias da semana permitidos (1=Segunda, 7=Domingo)")
    holidays: Optional[List[datetime]] = Field(default_factory=list,
                                               description="Lista de datas bloqueadas / feriados")
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator('end_time')
    def check_time_order(cls, v, info):
        start_time = info.data.get('start_time')
        if start_time and v <= start_time:
            raise ValueError('end_time deve ser maior que start_time')
        return v

    @field_validator('days_of_week')
    def check_days(cls, v):
        for day in v:
            if not 1 <= day <= 7:
                raise ValueError('days_of_week deve estar entre 1 e 7')
        return v


# CREATE TABLE reservation_config (
#     id TINYINT PRIMARY KEY DEFAULT 1,
#     start_time TIME NOT NULL,
#     end_time TIME NOT NULL,
#     slot_interval INT NOT NULL COMMENT 'Intervalo entre reservas em minutos',
#     min_reservation INT NOT NULL COMMENT 'Tempo mínimo de reserva em minutos',
#     max_reservation_days INT NOT NULL COMMENT 'Quantos dias no futuro é possível reservar',
#     days_of_week VARCHAR(20) DEFAULT '1,2,3,4,5' COMMENT 'Dias da semana permitidos, 1=Segunda',
#     holidays TEXT DEFAULT NULL COMMENT 'Datas bloqueadas/feriados separados por vírgula',
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# );
