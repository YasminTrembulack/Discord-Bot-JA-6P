from loguru import logger

from discord import Member
from discord.ext.commands import Cog, Bot

from models.user import UserPayload
from services.api_client import APIClient
from services.user_service import UserService


class EventsManager(Cog):
    bot: Bot
    _api_client: APIClient

    def __init__(self, bot, user_service):
        self.bot: Bot = bot
        self.user_service: UserService = user_service     

    @Cog.listener()
    async def on_ready(self):
        logger.info(f"✅ Bot online as {self.bot.user}")
    
        try:
            info = await self.bot._api_client.info()
            if info:
                logger.success(f"🌐 API respondeu com sucesso: {info}")
            else:
                logger.warning("⚠️ API não retornou dados válidos.")
        except Exception as e:
            logger.exception(f"❌ Erro ao chamar a API: {e}")

    @Cog.listener()
    async def on_member_join(self, member: Member):
        logger.info(f"👤 Novo membro entrou: {member.name} ({member.id})")
        try:
            await self.user_service.create_user(
            UserPayload(
                member_id=str(member.id),
                full_name=member.name,
                username=member.global_name,
                created_at=member.joined_at,
            ))
        except Exception as e:
            logger.exception(f"❌ Erro ao registrar usuário na API: {e}")


async def setup(bot):
    await bot.add_cog(EventsManager(bot))
