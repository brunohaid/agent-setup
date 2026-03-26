---
description: Plan the current task as a handover for a fresh session to implement
---
Write a handover that you'd want to receive if you were picking this up tomorrow with no memory of today.

**Mindset**: This is a first draft, not a specification. The implementing agent may see things you missed, find simpler approaches, or discover that an assumption was wrong. Write to enable that — flag uncertainty honestly, explain your reasoning so it can be questioned, and distinguish between "the user decided X" and "I'm proposing X".

**Study first**: Before proposing anything, spend the first half of your work just reading. Map the existing code that touches this feature. Find the simplest existing pattern that does something similar. Write a "Current State" section documenting what you found — not what you plan to build.

**Simplicity rule**: For each proposed change, ask: "Can this be done with fewer files, fewer abstractions, fewer new concepts?" If existing code is already convoluted, don't layer more on top — propose consolidating and simplifying it. The best plan often touches 1-3 files, adds no new architectural concepts, and leaves the codebase simpler than it found it.

**Verify before documenting**: Mark every assumption that hasn't been tested with `[UNVERIFIED]`. If your plan depends on a library behaving a certain way, an API accepting certain parameters, or a pattern working — say so explicitly. If there are more than 2-3 unverified assumptions, test them before finalizing the plan. A 5-minute REPL check beats a 2-hour implementation that discovers the premise was wrong.

**Content**: Trace all relevant code paths first. Then document: what we're building, why, what approach was chosen (and what was rejected), every file that needs changing, code sketches for non-obvious parts, and anything that should be verified before implementing.

**Location**: Save to the project's handovers directory (check for `docs/agents/handovers/` or similar). Include a `Started:` date and `Status: planning complete` header.

$@
