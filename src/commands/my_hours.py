"""
FileName : my_hours.py
FileInfo : This file contains the command for viewing a user's
           volunteer hours in the TMAS Academy Admin Bot.

           The /my-hours command retrieves and displays the
           volunteer hours logged by the user running the command.
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

class MyHours(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="my-hours",
        description="Show your volunteer-hour total, broken down by project."
    )
    async def my_hours(
        self,
        interaction: discord.Interaction
    ):
        pool = get_pool()

        async with pool.acquire() as db:
            project_totals = await db.fetch(
                """
                SELECT
                    projects.name,
                    SUM(hour_entries.hours)
                FROM hour_entries
                LEFT JOIN projects
                    ON hour_entries.project_id = projects.id
                WHERE hour_entries.user_id = $1
                GROUP BY hour_entries.project_id, projects.name
                ORDER BY projects.name IS NULL, projects.name
                """,
                interaction.user.id
            )

        if not project_totals:
            await interaction.response.send_message(
                "You have not logged any volunteer hours."
            )
            return

        total = sum(hours for _, hours in project_totals)

        lines = [
            "**Your Volunteer Hours**",
            f"**Total:** {format_hours(total)} hours",
            "**By Project**"
        ]

        for project_name, hours in project_totals:
            name = project_name or "No project"
            lines.append(f"**{name}:** {format_hours(hours)} hours")

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
    await bot.add_cog(MyHours(bot))