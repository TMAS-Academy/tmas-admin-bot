# TMAS Academy Admin Bot

The **TMAS Academy Admin Bot** is an internal Discord-based management system designed to support the organization's projects, tasks, team assignments, deadlines, and volunteer-hour tracking.

The bot provides a centralized workflow for managing organizational work directly within TMAS Academy's administrative Discord server.

---

## Overview

TMAS Academy operates across multiple teams and projects, including software engineering, academic writing, marketing, outreach, and other organizational initiatives.

The Admin Bot provides structure around that work by allowing administrators and team members to:

- Create and manage projects
- Create and assign tasks
- Track task status and priority
- Set deadlines and estimated work hours
- View individual task details
- Mark tasks as completed
- Track volunteer hours
- Associate work with specific projects
- Maintain persistent organizational records

The system is designed to be modular and extensible as TMAS Academy grows.

---

## Core Features

### Project Management

Projects provide a central organizational unit for related work.

Planned functionality includes:

- Creating projects
- Viewing all projects
- Viewing individual project details
- Associating tasks with projects
- Tracking work performed within a project
- Tracking volunteer hours by project

### Task Management

Tasks represent individual pieces of work assigned to TMAS Academy team members.

Each task can contain:

- Title
- Description
- Assignee
- Project
- Status
- Priority
- Deadline
- Estimated hours
- Creator
- Creation timestamp
- Completion timestamp

Supported task statuses:

```text
Not Started
In Progress
Blocked
Completed
```

Supported priorities:

```text
Low
Medium
High
```

### Task Assignment

Tasks can be assigned to individual Discord users.

This provides more detailed accountability than organizational roles alone.

For example, a team member may belong to:

```text
Marketing Team
```

while receiving individual tasks such as:

```text
Draft outreach email
Contact potential collaborators
Create Instagram announcement
Research partnership opportunities
```

This separates **organizational roles** from **specific responsibilities**.

### Deadline Tracking

Tasks can optionally include deadlines and estimated hours.

This allows the organization to track:

```text
What needs to be done
        ↓
Who is responsible
        ↓
When it is due
        ↓
How much work is expected
        ↓
Whether it has been completed
```

### Task Completion

Tasks can be explicitly marked as completed.

When a task is completed, the system records its completion timestamp, creating a persistent record of completed organizational work.

### Volunteer Hour Tracking

The Admin Bot includes a volunteer-hour tracking system designed to record contributions made by TMAS Academy team members.

Hour entries can be associated with:

- A user
- A task
- A project
- Number of hours
- Description of work
- Date

This provides a structured way to measure contributions across individual tasks and projects.

---

## Command System

The bot uses Discord slash commands.

### Project Commands

```text
/create-project
/projects
/project
```

These commands provide project creation, project discovery, and project-specific information.

### Task Commands

```text
/create-task
/task
/task-status
/complete-task
/my-tasks
```

These commands provide task creation, assignment, inspection, status management, and completion tracking.

### Volunteer Hour Commands

```text
/log-hours
/my-hours
/project-hours
```

These commands provide functionality for recording and reviewing volunteer contributions.

> Some commands are still under active development and will be integrated as development progresses.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core programming language |
| **discord.py** | Discord bot framework |
| **SQLite** | Persistent database |
| **aiosqlite** | Asynchronous SQLite access |
| **python-dotenv** | Environment variable management |
| **Git** | Version control |
| **GitHub** | Source control and collaboration |

---

## Architecture

The Admin Bot follows a modular command-based architecture using Discord Cogs.

```text
tmas-academy-admin-bot/
│
├── src/
│   ├── bot.py
│   ├── config.py
│   ├── database.py
│   │
│   └── commands/
│       ├── __init__.py
│       │
│       ├── projects.py
│       ├── create_project.py
│       ├── project.py
│       │
│       ├── create_task.py
│       ├── task.py
│       ├── task_status.py
│       ├── complete_task.py
│       └── my_tasks.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── tmas.db
```

Each command is separated into its own module to keep the codebase organized and make individual features easier to develop, test, and maintain.

---

## Database Architecture

The Admin Bot uses SQLite for persistent storage.

The current database is organized around three primary entities:

```text
Projects
   │
   └── Tasks
          │
          └── Hour Entries
```

### Projects

The `projects` table stores information about organizational projects.

```text
projects
├── id
├── name
├── description
├── created_by
└── created_at
```

### Tasks

The `tasks` table stores individual assignments.

```text
tasks
├── id
├── title
├── description
├── assignee_id
├── project_id
├── status
├── priority
├── deadline
├── estimated_hours
├── created_by
├── created_at
└── completed_at
```

### Hour Entries

The `hour_entries` table stores volunteer contributions.

```text
hour_entries
├── id
├── user_id
├── task_id
├── project_id
├── hours
├── description
├── date
└── created_at
```

Tasks reference projects, while hour entries can reference both tasks and projects.

This allows the system to maintain relationships between:

```text
Project
   ↓
Task
   ↓
Volunteer Work
```

---

## Configuration

The bot uses environment variables for sensitive configuration.

Create a `.env` file containing:

```env
DISCORD_TOKEN=your_discord_bot_token
GUILD_ID=your_discord_server_id
```

The `.env` file must **never be committed to GitHub**.

A `.env.example` file should be maintained to document required configuration variables without exposing credentials.

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd tmas-academy-admin-bot
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
DISCORD_TOKEN=your_discord_bot_token
GUILD_ID=your_discord_server_id
```

### 5. Run the Bot

```bash
python src/bot.py
```

The bot will initialize the database, load its command modules, connect to Discord, and synchronize its slash commands with the configured guild.

---

## Database Initialization

Database initialization is handled automatically when the bot starts.

The initialization process creates the required tables if they do not already exist.

This allows a fresh installation to initialize its database without requiring a separate database setup process.

---

## Development Workflow

Development follows a feature-branch workflow.

```text
                         main
                          │
             ┌────────────┼────────────┐
             │            │            │
             ▼            ▼            ▼
      feature/tasks  feature/projects  feature/hours
             │            │            │
             └────────────┼────────────┘
                          │
                          ▼
                     Pull Request
                          │
                          ▼
                         main
```

### Creating a Feature Branch

```bash
git checkout main
git pull origin main

git checkout -b feature/<feature-name>
```

### Committing Changes

```bash
git add .
git commit -m "Add <feature>"
```

### Pushing the Branch

```bash
git push -u origin feature/<feature-name>
```

A pull request can then be opened against `main`.

---

## Development Principles

### Modularity

Each major command should remain isolated in its own module whenever practical.

### Maintainability

Database operations and command logic should remain clear and understandable to future contributors.

### Persistence

Important organizational information should be stored persistently rather than relying on temporary Discord messages.

### Accountability

Every task should clearly communicate:

```text
What needs to be done
Who is responsible
Which project it belongs to
How important it is
When it is due
Whether it is complete
```

### Extensibility

The architecture should allow new organizational features to be added without requiring major restructuring of the existing application.

---

## Planned Improvements

The Admin Bot is an actively developing system.

Potential future functionality includes:

- [ ] Rich Discord embeds
- [ ] Interactive buttons and dropdowns
- [ ] Task filtering
- [ ] Task search
- [ ] Project dashboards
- [ ] Deadline reminders
- [ ] Overdue task detection
- [ ] Task statistics
- [ ] Volunteer-hour summaries
- [ ] Project progress summaries
- [ ] Administrative permissions
- [ ] Automated notifications
- [ ] Recurring tasks
- [ ] Reporting and analytics
- [ ] Exportable volunteer-hour reports
- [ ] Improved validation
- [ ] Automated testing

---

## Long-Term Architecture

The long-term goal is to turn the Admin Bot into a lightweight internal operations platform for TMAS Academy.

Rather than managing organizational work across disconnected systems:

```text
Discord Messages
Spreadsheets
Manual Checklists
Direct Messages
Separate Project Notes
```

the Admin Bot aims to provide a unified workflow:

```text
                         TMAS Academy
                               │
                         ┌─────┴─────┐
                         │  Projects │
                         └─────┬─────┘
                               │
                             Tasks
                               │
               ┌───────────────┼───────────────┐
               │               │               │
           Assignee         Deadline        Priority
               │               │               │
               └───────────────┼───────────────┘
                               │
                           Completion
                               │
                         Volunteer Hours
                               │
                         Project Reports
```

The system is intended to scale alongside the organization's projects, contributors, and operational needs.

---

## Project Status

**Status:** Active Development

The database architecture and core task-management functionality have been implemented.

Project-management and volunteer-hour functionality are being developed and integrated as the system progresses toward a complete internal release.

This README documents both the current architecture and the intended feature set of the completed system.

---

## Contributing

Development of the Admin Bot is currently limited to authorized TMAS Academy contributors.

Before beginning a feature:

1. Pull the latest `main` branch.
2. Create a dedicated feature branch.
3. Keep changes focused on the assigned feature.
4. Test the feature locally.
5. Commit using a descriptive commit message.
6. Push the feature branch.
7. Open a pull request.
8. Review and merge the changes into `main`.

When working on an isolated command, avoid unnecessarily modifying shared architecture files.

---

## License

This project is maintained by **TMAS Academy**.

See the repository license for applicable terms.

---

## TMAS Academy

The TMAS Academy Admin Bot is an internal software project developed to support the operations of **The Math and Science Academy (TMAS Academy)**.

TMAS Academy is a nonprofit organization focused on providing accessible STEM educational resources and opportunities to students.
