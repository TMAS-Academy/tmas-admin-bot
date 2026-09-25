"""
FileName : database.py
FileInfo : This file contains the database connection and
           initialization logic for the TMAS Academy Admin Bot.
"""

import aiosqlite

DATABASE_PATH = "tmas.db"

async def initialize_database():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        pass