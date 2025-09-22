import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from loguru import logger

from services.api_client import APIClient

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN']
API_BASE_URL = os.environ["API_URL"]

intents = discord.Intents.default()
intents.message_content = True


class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("cogs.reservation_calendar")


bot = MyBot(command_prefix="!", intents=intents)
api_client = APIClient(API_BASE_URL)


@bot.event
async def on_ready():
    logger.info(f"✅ Bot online as {bot.user}")
    
    try:
        info = await api_client.get_info()
        if info:
            logger.success(f"🌐 API respondeu com sucesso: {info}")
        else:
            logger.warning("⚠️ API não retornou dados válidos.")
    except Exception as e:
        logger.exception(f"❌ Erro ao chamar a API: {e}")


bot.run(TOKEN)

# https://discloud.com/
# https://squarecloud.app/pt-br/home
