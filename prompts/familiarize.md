---
description: Familiarize with a new project - analyze codebase and create agent documentation structure
---
Familiarize yourself with this project and set up documentation for future agent sessions.

## Step 1: Initial Exploration

Explore the project structure to understand:
- What kind of project is this? (web app, CLI tool, library, monorepo, etc.)
- What languages and frameworks are used?
- What's the directory structure?
- Are there existing docs, README, or configuration files?

```bash
# Useful commands to start
ls -la
find . -name "*.md" -type f | head -20
find . -type f -name "*.json" | xargs grep -l "dependencies" 2>/dev/null | head -5
```

## Step 2: Create Documentation Structure

Check if a documentation structure already exists (e.g., `docs/`, `.agent/`, `AGENTS.md`). If something similar is present, reuse and adapt it rather than creating a parallel structure.

If nothing exists, create the agent documentation folder structure:

```bash
mkdir -p docs/agents/context
mkdir -p docs/agents/handovers
mkdir -p docs/agents/deepdive
```

## Step 3: Create AGENTS.md

Create a root `AGENTS.md` file with:
- Quick start section pointing to context/handovers folders
- Project structure overview (directories and their purpose)
- Code style conventions (discover from existing code)
- Key commands (build, test, run, deploy)
- Important gotchas or patterns specific to this project

Keep it concise - this gets loaded on every session.

## Step 4: Create Context Files

In `docs/agents/context/`, create focused markdown files for major components. Each should be:
- Named after the component (e.g., `api.md`, `frontend.md`, `database.md`)
- 50-150 lines max - operational guidelines, not tutorials
- Focused on "what an agent needs to know to work here"

Include:
- Key file locations
- Important patterns and conventions
- Common operations (how to add X, where Y is configured)
- Gotchas specific to that component

## Step 5: Note What's NOT Needed Yet

- `handovers/` - Leave empty, used for incomplete work across sessions
- `deepdive/` - Leave empty, used for detailed analysis docs created on-demand

## Step 6: Report What You Created

Summarize:
- What you learned about the project
- What documentation you created
- Any areas that need deeper investigation later
- Suggested next steps for the user

**Do NOT commit changes. Just report what you created.**
