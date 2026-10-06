"""
FileName : complete_task.py
FileInfo : This file contains the command for completing a specific
           task in the TMAS Academy Admin Bot.

           This command marks a task as completed and records the
           time at which the task was completed.
"""

import discord
from discord import app_commands
from discord.ext import commands
from database import get_pool

class CompleteTask(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="complete-task",
        description="Mark a task as completed."
    )
    @app_commands.describe(
        task_id="The ID of the task to complete."
    )
    async def complete_task(
        self,
        interaction: discord.Interaction,
        task_id: int
    ):
        pool = get_pool()

        async with pool.acquire() as db:

            task = await db.fetchrow(
                """
                SELECT title, status
                FROM tasks
                WHERE id = $1
                """,
                task_id
            )

            if task is None:
                await interaction.response.send_message(
                    f"❌ Task #{task_id} does not exist."
                )
                return

            title = task["title"]
            status = task["status"]

            if status == "Completed":
                await interaction.response.send_message(
                    f"ℹ️ Task #{task_id} **{title}** is already completed."
                )
                return

            await db.execute(
                """
                UPDATE tasks
                SET status = 'Completed',
                    completed_at = CURRENT_TIMESTAMP
                WHERE id = $1
                """,
                task_id
            )

        await interaction.response.send_message(
            f"✅ Task #{task_id} **{title}** has been completed."
        )

async def setup(bot):
    await bot.add_cog(CompleteTask(bot))