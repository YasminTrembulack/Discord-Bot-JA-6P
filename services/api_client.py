import random
import uuid
from datetime import datetime, timezone
from typing import List

import aiohttp
from loguru import logger

from services.models import (
    EquipmentResponse,
    ReservationConfig,
    UserPayload,
    UserResponse,
)


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session: aiohttp.ClientSession | None = None

    async def start(self):
        """Cria a sessão ao iniciar o bot"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            logger.info("🌐 ClientSession inicializada")
    
    async def close(self):
        """Fecha a sessão ao desligar o bot"""
        if self.session:
            await self.session.close()
            logger.info("❌ ClientSession encerrada")

    async def get_info(self):
        if not self.session:
            raise RuntimeError("APIClient não iniciado. Chame start() antes.")
        
        async with self.session.get(f"{self.base_url}/") as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return f"{resp.status} | {self.base_url}/ - {await resp.text()}"
    
    async def create_reservation(self, user_id, date, start, end, status, equipment_id) -> uuid.UUID:
        logger.info(f"⏰ Reserva realizada por {user_id} para a {equipment_id} em {date} das {start} até {end} - Status: {status}")
        return uuid.uuid4() # deve retor o id da reserva criada

    async def update_reservation_status(self, reservation_id, status):
        logger.info(f"Status da reserva {reservation_id} atualizada. Status: {status}")

    async def get_unavailable_times_by_equipment(self, days: List[str], equipment_id):
        """ 
            Recebe no parametro uma lista de dias em datetime e id da maquina selecionada e manda para API
            API vai recerber e mandar os horarios indisponiveis nesses dias.
            Exemplo: {
                "24/09/2025": ["08:00", "09:00", "20:00"], 
                "25/09/2025": ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]
            }
        """
        logger.info(f"Buscando horarios indisponiveis do equipamento {equipment_id}")
        horarios = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]
        mock_response = { day: sorted(random.sample(horarios, 7)) for day in days }
        mock_response[days[0]] = horarios
        mock_response[days[-1]] = []
        return mock_response

    async def create_user(self, user: UserPayload):
        logger.success(f"✅ Usuário registrado na API: {user.model_dump()}")
        
    async def get_reservation_config(self):
        data = {
            "reservation_chanel": None, # "📅reservations"
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

    async def get_equipments(self) -> List[EquipmentResponse]:
        return [
            EquipmentResponse(
                id=uuid.uuid4(),
                name="3D Printer - Prusa i3 MK3S",
                description="Impressora 3D FDM, volume 250x210x210mm, nozzle 0.4mm",
                status="available",
                created_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
                updated_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
                deleted_at=None
            ),
            EquipmentResponse(
                id=uuid.uuid4(),
                name="3D Printer - Creality Ender 3",
                description="Impressora 3D FDM, volume 220x220x250mm, ideal para prototipagem rápida",
                status="in_use",
                created_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
                updated_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
                deleted_at=None
            ),
            EquipmentResponse(
                id=uuid.uuid4(),
                name="3D Printer - Formlabs Form 3",
                description="Impressora SLA de alta precisão para peças detalhadas",
                status="maintenance",
                created_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
                updated_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
                deleted_at=None
            ),
            EquipmentResponse(
                id=uuid.uuid4(),
                name="Laser Cutter - Glowforge Pro",
                description="Cortadora e gravadora a laser, área de corte 500x300mm, suporta acrílico e madeira",
                status="available",
                created_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
                updated_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
                deleted_at=None
            ),
        ]
        
    async def get_user(self, member_id, full_name, username) -> UserPayload:
        return UserResponse(
            id=uuid.uuid4(),
            member_id=member_id,
            username=username,
            full_name=full_name,
            created_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
            updated_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
            deleted_at=None)
