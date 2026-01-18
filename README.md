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
| [reflect](prompts/reflect.md) | End-of-session reflection - update docs and handovers |

### Extensions

| Extension | Description |
|-----------|-------------|
| [autoload-context](extensions/autoload-context.ts) | Auto-load `docs/agents/context/*.md` files into system prompt |

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
ln -s ~/agent-setup/prompts/reflect.md ~/.pi/agent/prompts/
```

Or copy them directly if you prefer.

## Usage

### PDF Skill

The skill loads automatically when working with PDFs, or invoke directly:

```
/skill:pdf
```

Requires `pdftotext` (install via `brew install poppler` on macOS).

### Reflect Prompt

Type `/reflect` at the end of a session to update handover docs and project documentation.
