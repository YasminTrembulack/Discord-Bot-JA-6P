import os
from cogs.reservation_manager import ReservationManager
from cogs.events import Events
import discord
from discord.ext import commands
from dotenv import load_dotenv

from services.api_client import APIClient
from services.user_service import UserService

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN']
API_BASE_URL = os.environ["API_URL"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._api_client = APIClient(API_BASE_URL)
        self.user_service = UserService(self._api_client)

    async def setup_hook(self):
        await self._api_client.start()
        
        await self.add_cog(ReservationManager(self, self.user_service))
        await self.add_cog(Events(self))

    async def close(self):
        await self._api_client.close()
        await super().close()


bot = MyBot(command_prefix="!", intents=intents)
bot.run(TOKEN)

@commands.command()
async def ping(self, ctx):
    await ctx.send("pong 🏓")
