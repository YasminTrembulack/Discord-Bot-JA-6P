import os
import aiohttp
from loguru import logger


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session: aiohttp.ClientSession | None = None

    async def start(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
            logger.info("🌐 ClientSession inicializada")
    
    async def close(self):
        if self.session:
            await self.session.close()
            logger.info("❌ ClientSession encerrada")

    async def info(self):
        return await self.get("/")
    
    async def get(self, endpoint: str):
        return await self._request("GET", endpoint)

    async def post(self, endpoint: str, json: dict):
        return await self._request("POST", endpoint, json=json)

    async def patch(self, endpoint: str, json: dict):
        return await self._request("PATCH", endpoint, json=json)
    
    async def put(self, endpoint: str, json: dict):
        return await self._request("PUT", endpoint, json=json)

    async def delete(self, endpoint: str):
        return await self._request("DELETE", endpoint)

    async def _request(self, method: str, endpoint: str, **kwargs):
        if not self.session:
            raise RuntimeError("⚠️ ClientSession não inicializada. Chame start() primeiro.")

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            async with self.session.request(method, url, **kwargs) as resp:
                try:
                    resp.raise_for_status()
                except aiohttp.ClientResponseError as e:
                    text = await resp.text()
                    logger.error(f"❌ Erro HTTP {e.status} em {url} → {text}")
                    return {"error": f"{e.status} {e.message}", "details": text}

                try:
                    return await resp.json()
                except aiohttp.ContentTypeError:
                    text = await resp.text()
                    logger.warning(f"⚠️ Resposta não JSON de {url}: {text[:200]}")
                    return {"raw": text}
                    
        except aiohttp.ClientError as e:
            logger.error(f"🚨 Erro de conexão com {url}: {e}")
            return {"error": "connection_error", "details": str(e)}
        except Exception as e:
            logger.exception(f"🔥 Erro inesperado em {url}")
            return {"error": "unexpected_error", "details": str(e)}

