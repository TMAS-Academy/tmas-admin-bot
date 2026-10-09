"""
FileName : project_hours.py
FileInfo : This file contains the command for viewing volunteer
           hours associated with a specific project in the TMAS
           Academy Admin Bot.

           The /project-hours command retrieves and displays the
           volunteer hours logged for a project identified by its ID.
"""

import discord
from discord import app_commands
from discord.ext import commands

from database import get_pool

DISCORD_MESSAGE_LIMIT = 2000

def format_hours(hours):
    rounded = round(float(hours), 2)

    if rounded == int(rounded):
        return str(int(rounded))

    return f"{rounded:.2f}".rstrip("0").rstrip(".")


class ProjectHours(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="project-hours",
        description="Show volunteer hours for a project, broken down by user."
    )
    @app_commands.describe(
        project_id="The ID of the project to look up."
    )
    async def project_hours(
        self,
        interaction: discord.Interaction,
        project_id: int
    ):
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message(
                "❌ You do not have permission to view project hours."
            )
            return

        pool = get_pool()

        async with pool.acquire() as db:
            project = await db.fetchrow(
                """
                SELECT name
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

            project_name = project["name"]

            user_totals = await db.fetch(
                """
                SELECT user_id, SUM(hours)
                FROM hour_entries
                WHERE project_id = $1
                GROUP BY user_id
                ORDER BY SUM(hours) DESC, user_id
                """,
                project_id
            )

        if not user_totals:
            await interaction.response.send_message(
                f"Project #{project_id} **{project_name}** has no logged "
                f"volunteer hours."
            )
            return

        total = sum(hours for _, hours in user_totals)

        lines = [
            f"**Volunteer Hours for {project_name}**",
            f"**Total:** {format_hours(total)} hours",
            "**By User**"
        ]

        for user_id, hours in user_totals:
            lines.append(
                f"**<@{user_id}>:** {format_hours(hours)} hours"
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
    await bot.add_cog(ProjectHours(bot))