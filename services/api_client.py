import aiohttp
from loguru import logger


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

    async def info(self):
        if not self.session:
            raise RuntimeError("APIClient não iniciado. Chame start() antes.")
        
        async with self.session.get(f"{self.base_url}/") as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return f"{resp.status} | {self.base_url}/ - {await resp.text()}"
    
    async def get(self, endpoint: str):
        async with self.session.get(f"{self.base_url}/{endpoint.lstrip('/')}") as resp:
            return await resp.json()
    
    async def post(self, endpoint: str, json: dict):
        async with self.session.post(f"{self.base_url}/{endpoint.lstrip('/')}", json=json) as resp:
            return await resp.json()
    
    async def patch(self, endpoint: str, json: dict):
        async with self.session.patch(f"{self.base_url}/{endpoint.lstrip('/')}", json=json) as resp:
            return await resp.json()
