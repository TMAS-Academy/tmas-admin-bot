"""
FileName : log_hours.py
FileInfo : This file contains the command for logging volunteer
           hours in the TMAS Academy Admin Bot.

           The /log-hours command records the number of hours
           contributed by a user and associates the entry with
           the relevant project or task.
"""

from typing import Optional
from datetime import datetime
import discord
from discord import app_commands
from discord.ext import commands
from database import get_pool

class LogHours(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="log-hours",
        description="Record volunteer hours for a project or task."
    )
    @app_commands.describe(
        hours="Number of volunteer hours to record.",
        date="Date the hours were worked.",
        description="What the hours were spent on.",
        project_id="Project these hours belong to.",
        task_id="Task these hours belong to."
    )
    async def log_hours(
        self,
        interaction: discord.Interaction,
        hours: float,
        date: str,
        description: str,
        project_id: Optional[int] = None,
        task_id: Optional[int] = None
    ):
        if hours <= 0:
            await interaction.response.send_message(
                "❌ Hours must be greater than 0."
            )
            return

        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d")
            if parsed_date.strftime("%Y-%m-%d") != date:
                raise ValueError
        except ValueError:
            await interaction.response.send_message(
                "❌ Invalid date. Use the format YYYY-MM-DD."
            )
            return

        if project_id is None and task_id is None:
            await interaction.response.send_message(
                "❌ Provide a project ID, a task ID, or both."
            )
            return

        pool = get_pool()

        async with pool.acquire() as db:
            project_name = None
            task_title = None

            if task_id is not None:
                task = await db.fetchrow(
                    """
                    SELECT tasks.title, tasks.project_id, projects.name
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

                task_title = task["title"]
                task_project_id = task["project_id"]
                task_project_name = task["name"]

                if project_id is not None and project_id != task_project_id:
                    await interaction.response.send_message(
                        f"❌ Task #{task_id} belongs to project "
                        f"#{task_project_id}, not project #{project_id}."
                    )
                    return

                project_id = task_project_id
                project_name = task_project_name

            else:
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

            # Volunteer hours stay in hour_entries. A task's
            # estimated_hours column is left unchanged.
            entry_id = await db.fetchval(
                """
                INSERT INTO hour_entries (
                    user_id,
                    task_id,
                    project_id,
                    hours,
                    description,
                    date
                )
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id
                """,
                interaction.user.id,
                task_id,
                project_id,
                hours,
                description,
                date
            )

        task_line = task_title if task_title is not None else "None"

        await interaction.response.send_message(
            f"**Hours Logged**\n"
            f"**ID:** {entry_id}\n"
            f"**Hours:** {hours}\n"
            f"**Date:** {date}\n"
            f"**Description:** {description}\n"
            f"**Project:** {project_name}\n"
            f"**Task:** {task_line}"
        )

async def setup(bot):
    await bot.add_cog(LogHours(bot))