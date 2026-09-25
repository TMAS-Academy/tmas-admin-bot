import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from database import initialize_database

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

async def setup_hook():
    await initialize_database()

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(DISCORD_TOKEN)