"""
FileName : database.py
FileInfo : This file contains the database connection and
           initialization logic for the TMAS Academy Admin Bot.
"""

import aiosqlite

DATABASE_PATH = "tmas.db"

async def initialize_database():
    async with aiosqlite.connect(DATABASE_PATH) as db:

        await db.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                assignee_id INTEGER NOT NULL,
                project_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'Not Started',
                priority TEXT NOT NULL DEFAULT 'Medium',
                deadline TEXT,
                estimated_hours REAL,
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS hour_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
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

        await db.commit()