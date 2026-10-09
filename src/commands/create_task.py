"""
FileName : create_task.py
FileInfo : This file contains the task creation logic and
           management commands for the TMAS Academy Admin Bot.
"""

import discord
from discord import app_commands
from discord.ext import commands

from database import get_pool


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
        pool = get_pool()

        async with pool.acquire() as db:

            # Make sure the project exists
            project = await db.fetchrow(
                """
                SELECT id, name
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

            # Create the task
            task_id = await db.fetchval(
                """
                INSERT INTO tasks (
                    title,
                    description,
                    assignee_id,
                    project_id,
                    deadline,
                    created_by
                )
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id
                """,
                title,
                description,
                assignee.id,
                project_id,
                deadline,
                interaction.user.id
            )

        await interaction.response.send_message(
            f"**Task Created**\n"
            f"**ID:** {task_id}\n"
            f"**Title:** {title}\n"
            f"**Project:** {project['name']}\n"
            f"**Assignee:** {assignee.mention}\n"
            f"**Deadline:** {deadline}"
        )

async def setup(bot):
    await bot.add_cog(CreateTask(bot))