from uuid import UUID, uuid4
from datetime import datetime, timezone
from loguru import logger
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

    async def get_user(self, member_id: str, full_name: str, username: str) -> UserResponse:
        """
        Busca o usuário na API. Se não existir, você poderia criar um novo usuário.
        """
        logger.info(f"🔍 Buscando usuário {member_id}")
        # Exemplo de requisição real:
        # response = await self.client.get(f"/users/{member_id}")
        # return UserResponse(**response)

        # Mock para testes:
        now = datetime.now(timezone.utc)
        return UserResponse(
            id=uuid4(),
            member_id=member_id,
            username=username,
            full_name=full_name,
            created_at=now,
            updated_at=now,
            deleted_at=None
        )

    async def update_user(self, user_id: UUID, payload: dict) -> UserResponse:
        """
        Atualiza dados de um usuário existente.
        """
        logger.info(f"✏️ Atualizando usuário {user_id} com {payload}")
        # Exemplo real:
        # response = await self.client.patch(f"/users/{user_id}", json=payload)
        # return UserResponse(**response)

        # Mock:
        now = datetime.now(timezone.utc)
        return UserResponse(
            id=user_id,
            member_id=payload.get("member_id", None),
            username=payload.get("username", None),
            full_name=payload.get("full_name", None),
            created_at=now,
            updated_at=now,
            deleted_at=None
        )
