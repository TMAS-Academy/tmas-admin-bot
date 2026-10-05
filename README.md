# TMAS Academy Admin Bot

An internal Discord management system for **TMAS Academy** that brings project management, task tracking, team assignments, deadlines, and volunteer-hour tracking into one centralized workflow.

Built with **Python, discord.py, and SQLite**, the bot uses a modular architecture that makes individual features easy to develop, test, and maintain.

---

## Overview

The TMAS Academy Admin Bot is designed to support the organization's internal operations across software engineering, academic writing, marketing, outreach, and other projects.

The bot provides functionality for:

- Creating and managing projects
- Creating and assigning tasks
- Tracking task status and priority
- Setting deadlines and estimated work hours
- Viewing individual task details
- Completing tasks and recording completion timestamps
- Viewing assigned tasks
- Recording volunteer hours
- Viewing personal volunteer hours
- Viewing project-level volunteer hours
- Maintaining persistent organizational records

The system is designed to provide a structured alternative to managing organizational work entirely through Discord messages, spreadsheets, and manual checklists.

---

## Features

### Project Management

Projects serve as the organizational unit for related work.

| Command | Description |
|---|---|
| `/create-project` | Create a new project |
| `/projects` | List all projects |
| `/project` | View information about a specific project |

Projects can contain multiple tasks and associated volunteer-hour entries.

### Task Management

Tasks represent individual pieces of work assigned to TMAS Academy contributors.

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

#### Task Statuses

```text
Not Started
In Progress
Blocked
Completed
```

#### Task Priorities

```text
Low
Medium
High
```

### Task Assignment

Tasks can be assigned directly to individual Discord users.

This separates **organizational roles** from **specific responsibilities**.

For example, a contributor may belong to the:

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

### Task Tracking

The bot provides commands for viewing and managing individual tasks:

| Command | Description |
|---|---|
| `/create-task` | Create and assign a task |
| `/task` | View detailed task information |
| `/my-tasks` | View tasks assigned to yourself |
| `/task-status` | Update a task's status |
| `/complete-task` | Mark a task as completed |

`/my-tasks` prioritizes tasks by **priority and deadline**, making it easier for contributors to identify what should be worked on next.

### Deadline Tracking

Tasks can optionally include:

- A deadline
- Estimated hours

This provides a structured workflow for understanding:

```text
What needs to be done
        ↓
Who is responsible
        ↓
When it is due
        ↓
How much work is expected
        ↓
Whether it is complete
```

### Task Completion

Tasks can be explicitly marked as completed.

When a task is completed, the database records its completion timestamp, creating a persistent record of organizational work.

### Volunteer Hour Tracking

The Admin Bot includes a volunteer-hour tracking system for recording contributions made by TMAS Academy team members.

Hour entries can be associated with:

- A user
- A task
- A project
- Number of hours
- Description of work
- Date

Available commands:

| Command | Description |
|---|---|
| `/log-hours` | Record volunteer hours |
| `/my-hours` | View your volunteer hours |
| `/project-hours` | View volunteer hours for a project |

Project-level volunteer-hour information is restricted to users with the appropriate Discord server permissions.

---

## Command Reference

### Projects

```text
/create-project
/projects
/project
```

### Tasks

```text
/create-task
/task
/task-status
/complete-task
/my-tasks
```

### Volunteer Hours

```text
/log-hours
/my-hours
/project-hours
```

All commands are implemented as Discord slash commands.

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

The bot uses a modular architecture based on **Discord Cogs**, with each major command isolated into its own module.

```text
tmas-admin-bot/
│
├── commands/
│   ├── __init__.py
│   │
│   ├── create_project.py
│   ├── projects.py
│   ├── project.py
│   │
│   ├── create_task.py
│   ├── task.py
│   ├── task_status.py
│   ├── complete_task.py
│   └── my_tasks.py
│   │
│   ├── log_hours.py
│   ├── my_hours.py
│   └── project_hours.py
│
├── bot.py
├── config.py
├── database.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

Each command is kept in its own module so that features can be developed independently without turning the bot into a single monolithic file.

The database connection and initialization logic are centralized in `database.py`, while `bot.py` handles bot startup, extension loading, and command synchronization.

---

## Database Architecture

The bot uses **SQLite** for persistent storage.

The database currently consists of three primary entities:

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

This structure allows the system to maintain relationships between:

```text
Project
   ↓
Task
   ↓
Volunteer Work
```

The database is initialized automatically when the bot starts. Required tables are created if they do not already exist.

---

## Configuration

The bot uses environment variables for sensitive configuration.

Create a `.env` file containing:

```env
DISCORD_TOKEN=your_discord_bot_token
GUILD_ID=your_discord_server_id
```

The `.env` file must **never be committed to GitHub**.

A `.env.example` file is included to document the required environment variables without exposing credentials.

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd tmas-admin-bot
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
python bot.py
```

On startup, the bot will:

1. Initialize the SQLite database
2. Load the command modules
3. Connect to Discord
4. Synchronize slash commands with the configured guild

---

## Development Workflow

Development follows a feature-branch and pull-request workflow.

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

### Create a Feature Branch

```bash
git switch main
git pull origin main
git switch -c feature/<feature-name>
```

### Make and Commit Changes

```bash
git add .
git commit -m "Add <feature>"
```

### Push the Branch

```bash
git push -u origin feature/<feature-name>
```

Open a pull request against `main` when the feature is ready for review.

### Development Guidelines

- Keep changes focused on the feature being implemented.
- Test commands locally before opening a pull request.
- Use descriptive commit messages.
- Avoid unnecessary modifications to shared architecture.
- Review pull requests before merging.
- Keep sensitive configuration out of version control.

---

## Development Principles

### Modularity

Each major command should remain isolated in its own module whenever practical.

### Maintainability

Database operations and command logic should remain clear and understandable to future contributors.

### Persistence

Important organizational information should be stored persistently rather than relying on temporary Discord messages.

### Accountability

Tasks should clearly communicate:

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

## Future Improvements

The core administrative workflow is implemented, but the system can continue to evolve.

Potential future improvements include:

- [ ] Rich Discord embeds
- [ ] Interactive buttons and dropdowns
- [ ] Task filtering and search
- [ ] Project dashboards
- [ ] Deadline reminders
- [ ] Overdue task detection
- [ ] Task statistics
- [ ] Volunteer-hour approval workflow
- [ ] Volunteer-hour summaries
- [ ] Project progress summaries
- [ ] More granular administrative permissions
- [ ] Automated notifications
- [ ] Recurring tasks
- [ ] Reporting and analytics
- [ ] Exportable volunteer-hour reports
- [ ] Automated testing

---

## Long-Term Vision

The long-term goal is to make the Admin Bot a lightweight internal operations platform for TMAS Academy.

Instead of managing organizational work across disconnected systems:

```text
Discord Messages
Spreadsheets
Manual Checklists
Direct Messages
Separate Project Notes
```

the Admin Bot provides a centralized workflow:

```text
                    TMAS Academy
                         │
                    ┌────┴────┐
                    │ Projects│
                    └────┬────┘
                         │
                       Tasks
                         │
          ┌──────────────┼──────────────┐
          │              │              │
      Assignee       Deadline       Priority
          │              │              │
          └──────────────┼──────────────┘
                         │
                     Completion
                         │
                   Volunteer Hours
                         │
                  Project Reporting
```

The system is intended to scale alongside TMAS Academy's projects, contributors, and operational needs.

---

## Project Status

**Status: Core Functionality Complete**

The Admin Bot currently provides the core functionality required for:

- Project management
- Task management
- Task assignment
- Task status tracking
- Task completion
- Deadline and priority tracking
- Volunteer-hour tracking
- Persistent SQLite storage

The architecture is now in a stable state for continued feature development and future improvements.

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
7. Open a pull request when appropriate.
8. Review the changes before merging into `main`.

When working on an isolated command, avoid unnecessarily modifying shared architecture files.

---

## License

This project is maintained by **TMAS Academy**.

See the repository license for applicable terms.

---

## TMAS Academy

The TMAS Academy Admin Bot is an internal software project developed to support the operations of **The Math and Science Academy (TMAS Academy)**.

TMAS Academy is a nonprofit organization focused on providing accessible STEM educational resources and opportunities to students.