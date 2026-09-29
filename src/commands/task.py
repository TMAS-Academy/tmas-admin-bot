"""
FileName : task.py
FileInfo : This file contains the command for viewing the details
           of a specific task in the TMAS Academy Admin Bot.

           This command retrieves and displays information for one
           task identified by its ID.
"""

import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from database import DATABASE_PATH

class Task(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="task",
        description="View a specific task's details"
    )
    async def task(
        self,
        interaction: discord.Interaction,
        task_id: int
    ):
        async with aiosqlite.connect(DATABASE_PATH) as db:
            cursor = await db.execute(
                """
                SELECT
                    tasks.id,
                    tasks.title,
                    tasks.description,
                    tasks.assignee_id,
                    projects.name,
                    tasks.status,
                    tasks.priority,
                    tasks.deadline,
                    tasks.estimated_hours,
                    tasks.created_by,
                    tasks.created_at,
                    tasks.completed_at
                FROM tasks
                JOIN projects
                    ON tasks.project_id = projects.id
                WHERE tasks.id = ?
                """,
                (task_id,)
            )

            task = await cursor.fetchone()

        if task is None:
            await interaction.response.send_message(
                f"❌ Task #{task_id} does not exist."
            )
            return

        (
            task_id,
            title,
            description,
            assignee_id,
            project_name,
            status,
            priority,
            deadline,
            estimated_hours,
            created_by,
            created_at,
            completed_at
        ) = task

        await interaction.response.send_message(
            f"**Task #{task_id}**\n"
            f"**Title:** {title}\n"
            f"**Description:** {description}\n"
            f"**Project:** {project_name}\n"
            f"**Assignee:** <@{assignee_id}>\n"
            f"**Status:** {status}\n"
            f"**Priority:** {priority}\n"
            f"**Deadline:** {deadline}\n"
            f"**Estimated Hours:** "
            f"{estimated_hours if estimated_hours is not None else 'None'}\n"
            f"**Created By:** <@{created_by}>\n"
            f"**Created At:** {created_at}\n"
            f"**Completed At:** {completed_at or 'Not completed'}"
        )

async def setup(bot):
    await bot.add_cog(Task(bot))