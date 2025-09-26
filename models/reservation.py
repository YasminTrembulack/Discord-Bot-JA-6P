from asyncio import Lock
from datetime import time, datetime
from typing import List, Literal, Optional
from uuid import UUID

from models.base import BaseResponse
from pydantic import BaseModel, Field, field_validator


class ReservationPayload(BaseModel):
    user_id: UUID = Field(..., description="ID do usuário que está fazendo a reserva")
    equipment_id: UUID = Field(..., description="ID do equipamento a ser reservado")
    responsible_id: Optional[UUID] = Field(None, description="ID do responsável pela aprovação")
    start: datetime = Field(..., description="Data e hora de início da reserva")
    end: datetime = Field(..., description="Data e hora de término da reserva")
    status: Literal['approved', 'rejected', 'pending'] = Field('pending',description="Status da reserva",)


class ReservationResponse(BaseResponse, ReservationPayload):
    pass


class UserReservationState:
    def __init__(self):
        self.lock = Lock()
        self.reservation: Optional[ReservationResponse] = None
        self.unavailable_time_slots = []
        self.equipment_name = None
        self.equipment_id = None
        self.start_time = None
        self.end_time = None
        self.date = None

  
class BotConfig(BaseModel):
    bot_id: str = Field(..., description="ID único do bot")
    opening_time: time = Field(..., description="Horário de término do funcionamento")
    closing_time: time = Field(..., description="Horário de início do funcionamento")
    min_reservation: int = Field(..., gt=0, description="Tempo mínimo de cada reserva em minutos")
    max_reservation_days: int = Field(..., gt=0, description="Quantos dias no futuro é possível reservar")
    max_reservation_blocks: int = Field(..., description="Quantos blocos de min_reservation podem ser encaixados em uma reserva (ex: 3).")
    holidays: Optional[List[datetime]] =  Field(default_factory=list, description="Lista de datas bloqueadas / feriados")
    days_of_week: List[int] = Field(default_factory=lambda: [1,2,3,4,5], description="Dias da semana permitidos (1=Segunda, 7=Domingo)")
    reservation_chanel: Optional[str] = Field(default=None, description="Nome do canal onde o bot vai ver a reservas, caso None lê todo os canais")
    reservation_approval_chanel: Optional[str] = Field(default=None, description="Nome do canal onde o bot vai mandas as reservas para aprovação, caso None ele entende que não precisa de aprovação")
    admin_roles: List[str] = Field(default_factory=list, description="IDs de roles de Admin do servidor")
    approver_roles: List[str] = Field(default_factory=list, description="IDs de roles que podem aprovar reservas")
    
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
