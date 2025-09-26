from datetime import datetime
import random
from typing import List
from uuid import UUID, uuid4
from loguru import logger
from services.api_client import APIClient
from types.models import ReservationConfig, ReservationPayload, ReservationResponse

class ReservationService:
    def __init__(self, client: APIClient):
        self.client = client

    async def get_reservation_config(self):
        data = {
            "reservation_chanel": "📅reservations", # "📅reservations"
            "reservation_approval_chanel": "📝pending-approval", # "📝pending-approval"
            "start_time": "08:00",
            "end_time": "21:00",
            "max_reservation_blocks": 2,
            "min_reservation": 60,
            "max_reservation_days": 7,
            "days_of_week": [1,2,3,4,5],
            "holidays": ["2025-12-25", "2025-09-25", "2025-01-01"]
        }

        # Conversão das strings para time / datetime
        data['start_time'] = datetime.strptime(data['start_time'], "%H:%M").time()
        data['end_time'] = datetime.strptime(data['end_time'], "%H:%M").time()
        data['holidays'] = [datetime.strptime(d, "%Y-%m-%d") for d in data['holidays']]

        # Criação da instância
        config = ReservationConfig(**data)
        return config
    
    async def create_reservation(self, reservation: ReservationPayload) -> UUID:
        logger.info(f"⏰ Reserva realizada:\n {reservation.model_dump()}")
        return uuid4() # deve retor o id da reserva criada
    
    async def fetch_unavailable_slots(self, next_days: List[str], equipment_id: UUID):
        logger.info(f"Buscando horarios indisponiveis do equipamento {equipment_id}")
        horarios = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]
        mock_response = { day: sorted(random.sample(horarios, 7)) for day in next_days }
        mock_response[next_days[0]] = horarios
        mock_response[next_days[-1]] = []
        return mock_response
    
    async def update_reservation(self, reservation: ReservationResponse) -> ReservationResponse:
        """
        Atualiza dados de um usuário existente.
        """
        logger.info(f"✏️ Atualizando reserva {reservation.id} com {reservation.status}")
        # Exemplo real:
        # response = await self.client.patch(f"/users/{user_id}", json=payload)
        # return UserResponse(**response)

        # Mock:
        return uuid4()