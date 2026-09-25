"""
FileName : projects.py
FileInfo : This file contains the project management
           commands for the TMAS Academy Admin Bot.
"""

import discord
import aiosqlite
from discord import app_commands
from discord.ext import commands
from database import DATABASE_PATH

class Projects(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="create-project",
        description="Create a new TMAS Academy project."
    )
    async def create_project(
        self,
        interaction: discord.Interaction,
        name: str,
        description: str
    ):
        async with aiosqlite.connect(DATABASE_PATH) as db:

            cursor = await db.execute(
                """
                INSERT INTO projects (
                    name,
                    description,
                    created_by
                )
                VALUES (?, ?, ?)
                """,
                (
                    name,
                    description,
                    interaction.user.id
                )
            )

            await db.commit()

            project_id = cursor.lastrowid

        await interaction.response.send_message(
            f"**Project Created**\n"
            f"**ID:** {project_id}\n"
            f"**Name:** {name}\n"
            f"**Description:** {description}"
        )

async def setup(bot):
    await bot.add_cog(Projects(bot))