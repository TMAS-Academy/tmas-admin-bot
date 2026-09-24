import discord
from discord.ext import commands
from config import DISCORD_TOKEN

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()
    print("Slash commands synced.")

bot.run(DISCORD_TOKEN)