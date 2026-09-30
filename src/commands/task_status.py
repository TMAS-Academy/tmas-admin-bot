"""
FileName : task_status.py
FileInfo : This file contains the command for updating the status
           of a specific task in the TMAS Academy Admin Bot.

           This command allows a user to change a task's status
           between the supported task statuses.
"""

import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from database import DATABASE_PATH

class TaskStatus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="task-status",
        description="Update the status of a specific task."
    )
    @app_commands.describe(
        task_id="The ID of the task to update.",
        status="The new status for the task."
    )
    async def task_status(
        self,
        interaction: discord.Interaction,
        task_id: int,
        status: str
    ):
        valid_statuses = {
            "Not Started",
            "In Progress",
            "Blocked",
            "Completed"
        }

        if status not in valid_statuses:
            await interaction.response.send_message(
                "❌ Invalid status. Choose one of: "
                "Not Started, In Progress, Blocked, Completed."
            )
            return

        async with aiosqlite.connect(DATABASE_PATH) as db:
            cursor = await db.execute(
                """
                SELECT title
                FROM tasks
                WHERE id = ?
                """,
                (task_id,)
            )

            task = await cursor.fetchone()

            if task is None:
                await interaction.response.send_message(
                    f"❌ Task #{task_id} does not exist."
                )
                return

            await db.execute(
                """
                UPDATE tasks
                SET status = ?
                WHERE id = ?
                """,
                (status, task_id)
            )

            await db.commit()

        await interaction.response.send_message(
            f"✅ Task #{task_id} **{task[0]}** status updated to "
            f"**{status}**."
        )


async def setup(bot):
    await bot.add_cog(TaskStatus(bot))