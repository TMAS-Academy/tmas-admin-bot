"""
FileName : create_project.py
FileInfo : This file contains the command for creating a new
           project in the TMAS Academy Admin Bot.

           The /create-project command creates and stores a new
           project in the database.
"""

import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from database import DATABASE_PATH


class CreateProject(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="create-project",
        description="Create a new project."
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
                INSERT INTO projects (name, description, created_by)
                VALUES (?, ?, ?)
                """,
                (
                    name,
                    description,
                    interaction.user.id
                )
            )

            project_id = cursor.lastrowid

            await db.commit()

        await interaction.response.send_message(
            f"**Project Created**\n"
            f"**ID:** {project_id}\n"
            f"**Name:** {name}\n"
            f"**Description:** {description}"
        )


async def setup(bot):
    await bot.add_cog(CreateProject(bot))
