from uuid import uuid4
from loguru import logger
from datetime import datetime, timezone
from models.user import UserPayload, UserResponse
from services.api_client import APIClient

class UserService:
    def __init__(self, client: APIClient):
        self.client = client

    async def create_user(self, user: UserPayload) -> UserResponse:
        """
        Cria um usuário na API e retorna os dados do usuário criado.
        """
        logger.info(f"✅ Registrando usuário: {user.model_dump()}")
        # Aqui você chamaria algo como:
        # response = await self.client.post("/users", json=user.dict())
        # return UserResponse(**response)

        # Mock para testes:
        now = datetime.now(timezone.utc)
        return UserResponse(
            id=uuid4(),
            member_id=user.member_id,
            username=user.username,
            full_name=user.full_name,
            created_at=now,
            updated_at=now,
            deleted_at=None
        )

    async def get_user(self, user: UserPayload) -> UserResponse:
        """
        Busca o usuário na API. Se não existir, você poderia criar um novo usuário.
        """
        logger.info(f"🔍 Buscando usuário {user.member_id}")
        # Exemplo de requisição real:
        # response = await self.client.get(f"/users/{member_id}")
        # return UserResponse(**response)

        # Mock para testes:
        now = datetime.now(timezone.utc)
        return UserResponse(
            id=uuid4(),
            member_id=user.member_id,
            username=user.username,
            full_name=user.full_name,
            created_at=now,
            updated_at=now,
            deleted_at=None
        )

    async def update_user(self, user: UserResponse) -> UserResponse:
        """
        Atualiza dados de um usuário existente.
        """
        logger.info(f"✏️ Atualizando usuário {user.id} com {user.model_dump()}")
        # Exemplo real:
        # response = await self.client.patch(f"/users/{user_id}", json=payload)
        # return UserResponse(**response)
        return uuid4()
