import aiohttp
from loguru import logger

from services.models import User

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
    
    async def create_reservation(self, user_id, date, start, end):
        ...

    async def update_reservation_status(self, reservation_id, status):
        ...

    async def get_reservations(self, date: str):
        ...
        
    async def register_user(self, user: User):
        # if not self.session:
        #     raise RuntimeError("APIClient não iniciado. Chame start() antes.")

        # try:
        #     async with self.session.post(f"{self.base_url}/users/", json=user.model_dump()) as resp:
        #         if resp.status == 201:
        #             return await resp.json()
        #         else:
        #             text = await resp.text()
        #             logger.error(f"Erro {resp.status} ao registrar usuário: {text}")
        #             return None
        # except Exception as e:
        #     logger.exception(f"Erro de conexão com API: {e}")
        #     return None
        logger.success(f"✅ Usuário registrado na API: {user.model_dump()}")
