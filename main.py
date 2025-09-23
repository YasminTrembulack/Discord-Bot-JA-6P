import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from services.api_client import APIClient

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN']
API_BASE_URL = os.environ["API_URL"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_client = APIClient(API_BASE_URL)

    async def setup_hook(self):
        await self.api_client.start()  # 🔹 inicia a sessão
        await self.load_extension("cogs.reservation_calendar")
        await self.load_extension("cogs.events")

    async def close(self):
        await self.api_client.close()  # 🔹 fecha a sessão antes de encerrar
        await super().close()


bot = MyBot(command_prefix="!", intents=intents)
bot.run(TOKEN)
