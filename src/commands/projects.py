"""
FileName : projects.py
FileInfo : This file contains the project management
           commands for the TMAS Academy Admin Bot.
"""

import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from database import DATABASE_PATH

class Projects(commands.Cog):

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

    @app_commands.command(
        name="projects",
        description="List all projects."
    )
    async def list_projects(
        self,
        interaction: discord.Interaction
    ):
        async with aiosqlite.connect(DATABASE_PATH) as db:
            cursor = await db.execute(
                """
                SELECT id, name, description
                FROM projects
                ORDER BY id
                """
            )

            projects = await cursor.fetchall()

        if not projects:
            await interaction.response.send_message(
                "There are no projects yet."
            )
            return

        lines = ["**Projects**"]

        for project_id, name, description in projects:
            lines.append(
                f"**{project_id}. {name}**\n"
                f"{description}"
            )

        await interaction.response.send_message(
            "\n\n".join(lines)
        )

async def setup(bot):
    await bot.add_cog(Projects(bot))