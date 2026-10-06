"""
FileName : database.py
FileInfo : This file contains the database connection and
           initialization logic for the TMAS Academy Admin Bot.
"""

import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

from config import DATABASE_URL
_pool = None

async def initialize_database():
    global _pool

    _pool = await asyncpg.create_pool(DATABASE_URL)

    async with _pool.acquire() as db:

        await db.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                created_by BIGINT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                assignee_id BIGINT NOT NULL,
                project_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'Not Started',
                priority TEXT NOT NULL DEFAULT 'Medium',
                deadline TEXT,
                estimated_hours REAL,
                created_by BIGINT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS hour_entries (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                task_id INTEGER,
                project_id INTEGER,
                hours REAL NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (task_id) REFERENCES tasks(id),
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        """)

def get_pool():
    return _pool