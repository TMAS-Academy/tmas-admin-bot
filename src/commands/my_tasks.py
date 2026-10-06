"""
FileName : my_tasks.py
FileInfo : This file contains the command for viewing tasks
           assigned to the current user in the TMAS Academy
           Admin Bot.

           The /my-tasks command retrieves and displays the tasks
           assigned to the user running the command.
"""

import discord
from discord import app_commands
from discord.ext import commands
from database import get_pool

DISCORD_MESSAGE_LIMIT = 2000

class MyTasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="my-tasks",
        description="Show all tasks assigned to you."
    )
    async def my_tasks(
        self,
        interaction: discord.Interaction
    ):
        pool = get_pool()

        async with pool.acquire() as db:
            tasks = await db.fetch(
                """
                SELECT
                    tasks.id,
                    tasks.title,
                    projects.name,
                    tasks.status,
                    tasks.priority,
                    tasks.deadline
                FROM tasks
                JOIN projects
                    ON tasks.project_id = projects.id
                WHERE tasks.assignee_id = $1
                ORDER BY
                    CASE tasks.priority
                        WHEN 'High' THEN 1
                        WHEN 'Medium' THEN 2
                        WHEN 'Low' THEN 3
                        ELSE 4
                    END,
                    tasks.deadline IS NULL,
                    tasks.deadline,
                    tasks.id
                """,
                interaction.user.id
            )

        if not tasks:
            await interaction.response.send_message(
                "You have no assigned tasks."
            )
            return

        lines = ["**Your Tasks**"]

        for task_id, title, project_name, status, priority, deadline in tasks:
            lines.append(
                f"**#{task_id}. {title}**\n"
                f"**Project:** {project_name}\n"
                f"**Status:** {status}\n"
                f"**Priority:** {priority}\n"
                f"**Deadline:** {deadline or 'None'}"
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
    await bot.add_cog(MyTasks(bot))