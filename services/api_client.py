from loguru import logger
import aiohttp
import os

API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL

    async def get_info(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/") as resp:
                if resp.status == 200:
                    response = await resp.json()
                    logger.info(f"Resposta da API: {response}")
                    return response
                else:
                    text = await resp.text()
                    logger.error(f"Erro {resp.status} ao acessar {self.base_url}/ - {text}")
                    return None
    
    async def create_reservation(self, user_id, date, start, end):
        async with aiohttp.ClientSession() as session:
            payload = {
                "user_id": user_id,
                "date": date,
                "start_time": start,
                "end_time": end,
            }
            async with session.post(f"{self.base_url}/reservations/", json=payload) as resp:
                return await resp.json()

    async def update_reservation_status(self, reservation_id, status):
        async with aiohttp.ClientSession() as session:
            async with session.patch(f"{self.base_url}/reservations/{reservation_id}/", json={"status": status}) as resp:
                return await resp.json()

    async def get_reservations(self, date: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/reservations/?date={date}") as resp:
                return await resp.json()
