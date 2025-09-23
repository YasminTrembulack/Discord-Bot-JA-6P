import discord
from loguru import logger
from services.models import User
from discord.ext.commands import Cog


class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        logger.info(f"✅ Bot online as {self.bot.user}")
    
        try:
            info = await self.bot.api_client.get_info()
            if info:
                logger.success(f"🌐 API respondeu com sucesso: {info}")
            else:
                logger.warning("⚠️ API não retornou dados válidos.")
        except Exception as e:
            logger.exception(f"❌ Erro ao chamar a API: {e}")

    @Cog.listener()
    async def on_member_join(self, member: discord.Member):
        logger.info(f"👤 Novo membro entrou: {member.name} ({member.id})")
        try:
            await self.bot.api_client.register_user(
            User(
                member_id=str(member.id),
                full_name=member.name,
                username=member.global_name,
                created_at=member.joined_at,
            ))
        except Exception as e:
            logger.exception(f"❌ Erro ao registrar usuário na API: {e}")


async def setup(bot):
    await bot.add_cog(Events(bot))
