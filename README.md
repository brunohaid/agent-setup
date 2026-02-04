# Agent Setup

Skills and prompts for [pi](https://github.com/mariozechner/pi-coding-agent).

## Contents

### Skills

| Skill | Description |
|-------|-------------|
| [pdf](skills/pdf/SKILL.md) | Extract text and tables from PDFs using pdftotext (simple) or pdfplumber (advanced) |

### Prompts

| Prompt | Description |
|--------|-------------|
| [familiarize](prompts/familiarize.md) | Get oriented with a new codebase |
| [improve](prompts/improve.md) | Suggest structural improvements to docs/agents organization |
| [recall](prompts/recall.md) | Search for relevant past learnings not loaded at session start |
| [reflect](prompts/reflect.md) | End-of-session reflection - update docs and handovers |
| [weigh](prompts/weigh.md) | Weigh session discussion and propose 3 solutions with pros and cons |

### Extensions

| Extension | Description |
|-----------|-------------|
| [autoload-context](extensions/autoload-context.ts) | Auto-load `docs/agents/context/*.md` files into system prompt |
| [self-update](extensions/self-update.ts) | Update pi and restart with current session via `/update` command |

## Installation

### Skills

Clone this repo and add to your pi settings:

```bash
git clone https://github.com/brunohaid/agent-setup ~/agent-setup
```

Edit `~/.pi/agent/settings.json`:

```json
{
  "skills": {
    "customDirectories": ["~/agent-setup/skills"]
  }
}
```

### Prompts

Symlink prompts to your pi prompts directory:

```bash
mkdir -p ~/.pi/agent/prompts
ln -s ~/agent-setup/prompts/*.md ~/.pi/agent/prompts/
```

Or symlink individually / copy them directly if you prefer.

### Extensions

Symlink extensions to your pi extensions directory:

```bash
mkdir -p ~/.pi/agent/extensions
ln -s ~/agent-setup/extensions/*.ts ~/.pi/agent/extensions/
```

## Usage

### PDF Skill

The skill loads automatically when working with PDFs, or invoke directly:

```
/skill:pdf
```

Requires `pdftotext` (install via `brew install poppler` on macOS).

### Prompts

- `/familiarize` - Get oriented with a new codebase
- `/improve` - Suggest improvements to docs/agents organization  
- `/recall` - Search for relevant past learnings
- `/reflect` - End-of-session reflection and doc updates
- `/weigh` - Propose 3 solutions with pros and cons for current discussion

### Self-Update

Run `/update` to update pi to the latest version and automatically restart with your current session. No manual restart required.
