"""
FileName : create_task.py
FileInfo : This file contains the task creation logic and
           management commands for the TMAS Academy Admin Bot.
"""

import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from database import DATABASE_PATH

class CreateTask(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="create-task",
        description="Create a new team task."
    )
    async def create_task(
        self,
        interaction: discord.Interaction,
        title: str,
        description: str,
        project_id: int,
        assignee: discord.Member,
        deadline: str
    ):
        async with aiosqlite.connect(DATABASE_PATH) as db:

            # Make sure the project exists
            cursor = await db.execute(
                """
                SELECT id, name
                FROM projects
                WHERE id = ?
                """,
                (project_id,)
            )

            project = await cursor.fetchone()

            if project is None:
                await interaction.response.send_message(
                    f"❌ Project #{project_id} does not exist."
                )
                return

            # Create the task
            cursor = await db.execute(
                """
                INSERT INTO tasks (
                    title,
                    description,
                    assignee_id,
                    project_id,
                    deadline,
                    created_by
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    title,
                    description,
                    assignee.id,
                    project_id,
                    deadline,
                    interaction.user.id
                )
            )

            task_id = cursor.lastrowid

            await db.commit()

        await interaction.response.send_message(
            f"**Task Created**\n"
            f"**ID:** {task_id}\n"
            f"**Title:** {title}\n"
            f"**Project:** {project[1]}\n"
            f"**Assignee:** {assignee.mention}\n"
            f"**Deadline:** {deadline}"
        )

async def setup(bot):
    await bot.add_cog(CreateTask(bot))