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
from database import get_pool

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
        pool = get_pool()

        async with pool.acquire() as db:
            task = await db.fetchrow(
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
                WHERE tasks.id = $1
                """,
                task_id
            )

        if task is None:
            await interaction.response.send_message(
                f"❌ Task #{task_id} does not exist."
            )
            return

        await interaction.response.send_message(
            f"**Task #{task['id']}**\n"
            f"**Title:** {task['title']}\n"
            f"**Description:** {task['description']}\n"
            f"**Project:** {task['name']}\n"
            f"**Assignee:** <@{task['assignee_id']}>\n"
            f"**Status:** {task['status']}\n"
            f"**Priority:** {task['priority']}\n"
            f"**Deadline:** {task['deadline']}\n"
            f"**Estimated Hours:** "
            f"{task['estimated_hours'] if task['estimated_hours'] is not None else 'None'}\n"
            f"**Created By:** <@{task['created_by']}>\n"
            f"**Created At:** {task['created_at']}\n"
            f"**Completed At:** {task['completed_at'] or 'Not completed'}"
        )

async def setup(bot):
    await bot.add_cog(Task(bot))