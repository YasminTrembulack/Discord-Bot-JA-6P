from uuid import uuid4
from loguru import logger
from datetime import datetime, timezone
from models.user import UserPayload, UserResponse
from services.api_client import APIClient


class UserService:
    def __init__(self, client: APIClient):
        self.client = client

    async def create_user(self, user: UserPayload) -> UserResponse:
        user_json = user.model_dump()
        logger.info(f"✅ Registrando usuário: {user_json}")

        response = await self.client.post("/api/users/register", json=user_json)

        return UserResponse(**response)

    async def get_user(self, discord_id: str) -> UserResponse:
        """
        Busca o usuário na API. Se não existir, você poderia criar um novo usuário.
        """
        logger.info(f"🔍 Buscando usuário {discord_id}")
        # Exemplo de requisição real:
        response = await self.client.get(f"/api/users/{discord_id}")
        
        return [UserResponse(**r) for r in response]


    async def update_user(self, user: UserResponse) -> UserResponse:
        """
        Atualiza dados de um usuário existente.
        """
        logger.info(f"✏️ Atualizando usuário {user.id} com {user.model_dump()}")
        # Exemplo real:
        # response = await self.client.patch(f"/users/{user_id}", json=payload)
        # return UserResponse(**response)
        return uuid4()
