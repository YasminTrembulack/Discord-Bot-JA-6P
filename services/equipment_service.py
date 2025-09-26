from typing import List
from uuid import uuid4
from datetime import datetime, timezone
from models.equipment import EquipmentResponse
from services.api_client import APIClient

class EquipmentService:
    def __init__(self, client: APIClient):
        self.client = client
        
    async def get_equipments(self) -> List[EquipmentResponse]:
        return [
            EquipmentResponse(
                id=uuid4(),
                name="3D Printer - Prusa i3 MK3S",
                description="Impressora 3D FDM, volume 250x210x210mm, nozzle 0.4mm",
                status="available",
                created_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
                updated_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
                deleted_at=None
            ),
            EquipmentResponse(
                id=uuid4(),
                name="3D Printer - Creality Ender 3",
                description="Impressora 3D FDM, volume 220x220x250mm, ideal para prototipagem rápida",
                status="in_use",
                created_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
                updated_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
                deleted_at=None
            ),
            EquipmentResponse(
                id=uuid4(),
                name="3D Printer - Formlabs Form 3",
                description="Impressora SLA de alta precisão para peças detalhadas",
                status="maintenance",
                created_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
                updated_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
                deleted_at=None
            ),
            EquipmentResponse(
                id=uuid4(),
                name="Laser Cutter - Glowforge Pro",
                description="Cortadora e gravadora a laser, área de corte 500x300mm, suporta acrílico e madeira",
                status="available",
                created_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
                updated_at=datetime(2025, 9, 25, 13, 34, 0, 710742, tzinfo=timezone.utc),
                deleted_at=None
            ),
        ]
