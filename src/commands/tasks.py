"""
FileName : tasks.py
FileInfo : This file contains the task management
           commands for the TMAS Academy Admin Bot.
"""

import discord
from discord import app_commands
from discord.ext import commands

class Tasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="create-task",
        description="Create a new team task."
    )
    async def create_task(
        self,
        interaction: discord.Interaction,
        title: str,
        description: str
    ):
        await interaction.response.send_message(
            f"**Task Created**\n"
            f"**Title:** {title}\n"
            f"**Description:** {description}"
        )

async def setup(bot):
    await bot.add_cog(Tasks(bot))