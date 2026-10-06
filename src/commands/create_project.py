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
from database import get_pool

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
        pool = get_pool()

        async with pool.acquire() as db:
            project_id = await db.fetchval(
                """
                INSERT INTO projects (name, description, created_by)
                VALUES ($1, $2, $3)
                RETURNING id
                """,
                name,
                description,
                interaction.user.id
            )

        await interaction.response.send_message(
            f"**Project Created**\n"
            f"**ID:** {project_id}\n"
            f"**Name:** {name}\n"
            f"**Description:** {description}"
        )

async def setup(bot):
    await bot.add_cog(CreateProject(bot))