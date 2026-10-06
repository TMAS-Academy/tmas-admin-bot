"""
FileName : project.py
FileInfo : This file contains the command for viewing the details
           of a specific project in the TMAS Academy Admin Bot.

           This is separate from projects.py, which handles listing
           multiple projects. The /project command retrieves and
           displays information for one project identified by its ID.
"""

import discord
from discord import app_commands
from discord.ext import commands
from database import get_pool

class Project(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="project",
        description="View the details of a specific project."
    )
    @app_commands.describe(
        project_id="The ID of the project to view."
    )
    async def project(
        self,
        interaction: discord.Interaction,
        project_id: int
    ):
        pool = get_pool()

        async with pool.acquire() as db:
            project = await db.fetchrow(
                """
                SELECT
                    id,
                    name,
                    description,
                    created_by,
                    created_at
                FROM projects
                WHERE id = $1
                """,
                project_id
            )

        if project is None:
            await interaction.response.send_message(
                f"❌ Project #{project_id} does not exist."
            )
            return

        await interaction.response.send_message(
            f"**Project #{project['id']}**\n"
            f"**Name:** {project['name']}\n"
            f"**Description:** {project['description'] or 'None'}\n"
            f"**Created By:** <@{project['created_by']}>\n"
            f"**Created At:** {project['created_at']}"
        )

async def setup(bot):
    await bot.add_cog(Project(bot))