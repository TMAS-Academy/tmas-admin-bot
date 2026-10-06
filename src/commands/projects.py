"""
FileName : projects.py
FileInfo : This file contains the command for listing projects
           in the TMAS Academy Admin Bot.

           The /projects command retrieves and displays every
           project stored in the database.
"""

import discord
from discord import app_commands
from discord.ext import commands
from database import get_pool

DISCORD_MESSAGE_LIMIT = 2000

class Projects(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="projects",
        description="List all projects."
    )
    async def list_projects(
        self,
        interaction: discord.Interaction
    ):
        pool = get_pool()

        async with pool.acquire() as db:
            projects = await db.fetch(
                """
                SELECT id, name, description
                FROM projects
                ORDER BY id
                """
            )

        if not projects:
            await interaction.response.send_message(
                "There are no projects yet."
            )
            return

        lines = ["**Projects**"]

        for project_id, name, description in projects:
            lines.append(
                f"**{project_id}. {name}**\n"
                f"{description or 'No description'}"
            )

        chunks = []
        current = ""

        for line in lines:
            piece = line if not current else f"\n\n{line}"

            if len(current) + len(piece) > DISCORD_MESSAGE_LIMIT:
                chunks.append(current)
                current = line
            else:
                current += piece

        if current:
            chunks.append(current)

        await interaction.response.send_message(chunks[0])

        for chunk in chunks[1:]:
            await interaction.followup.send(chunk)

async def setup(bot):
    await bot.add_cog(Projects(bot))