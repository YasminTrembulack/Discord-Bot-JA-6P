import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN']

intents = discord.Intents.default()
intents.message_content = True


class MyBot(commands.Bot):

    async def setup_hook(self):
        await self.load_extension("cogs.reservation_calendar")


bot = MyBot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logger.info(f"✅ Bot online as {bot.user}")


bot.run(TOKEN)

# https://discloud.com/
# https://squarecloud.app/pt-br/home
