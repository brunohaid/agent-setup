---
description: End-of-session reflection - update docs and handovers
---
Reflect on what was learned and accomplished in this session:

1. **Session summary**:
   - Briefly summarize what was accomplished this session

2. **Learn from mistakes**:
   - If you struggled, made multiple failed attempts, or hit unexpected bugs, identify the root cause
   - Distill this into a brief lesson: what assumption was wrong? What should you check first next time?
   - If the user got frustrated, distill why and how this can be avoided in the future

3. **Journal entry** (if docs/agents/journal/ exists):
   - Create a file with format: `YYYY-MM-DD-HHMM-very-short-summary.md`
   - Example: `2026-02-01-1622-fixed-auth-bug.md`
   - Content: Brief session summary - what was done, key decisions, outcomes
   - Keep it concise (5-15 lines) - this is for quick recall, not detailed docs

4. **Handover files** (if the project has a handovers directory):
   - Update existing handover files if you made progress on that work
   - **Never update handovers in `completed/` subdirectory** - those are archived historical records
   - **Evolve, don't overwrite**: Update understanding as you learn, but preserve what was tried and why it failed/worked. The handover should reflect current knowledge while keeping a record of the problem-solving journey. The final handover should tell the full story: what was tried, what failed, what worked.
   - For ongoing work: document what was tried this session, what worked/failed, current state
   - For completed work: ensure the handover captures the journey, then suggest archiving to user (use `git mv` to move to `completed/`)
   - Timestamps: `Started: YYYY-MM-DD` when creating, `Updated: YYYY-MM-DD` when modifying, `Completed: YYYY-MM-DD` when archiving
   - Only create a NEW handover if there's complex incomplete work that would be hard to continue without context (rare - maybe 1 in 20 sessions)

5. **Reference files** (loaded on demand, usually in docs/agents/reference):
   - List the reference directory contents
   - Check if any existing file relates to this session's topic
   - If yes: update it with new knowledge, gotchas, or patterns discovered
   - If no relevant file exists but the session involved significant learning about a specific technology/system that will be used again: propose creating a new reference file (rare - only for substantial, reusable knowledge)

6. **Agent documentation** (AGENTS.md and auto-loaded context files):
   - Review all context files that were loaded at session start - can any be improved based on this session?
   - Update if there's a new learning, convention, gotcha, or pattern that should apply across all future sessions
   - Examples: "always check X before Y", "this codebase does Z differently", "avoid approach W because..."
   - Be conservative - only add lessons that would have saved significant time/effort or improved the outcome had you known them at session start
   - Keep it focused - detailed info should already be in handovers/reference files by now

Summarize what you're updating and why. If nothing needs updating, say so.

**Do NOT commit or push changes. Just report what you updated.**

$@
