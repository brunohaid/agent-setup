---
description: Recall past learnings not loaded at session start
---
Search for relevant knowledge we've already captured but didn't autoload into this session:

1. **Identify keywords**: List 3-5 terms from the current task (technologies, error messages, file names, concepts)

2. **Search with context**:
   ```bash
   grep -ri -C 10 "<term>" docs/agents/
   ```
   This shows 10 lines around each match - enough to understand without loading entire files.

3. **Scan results for**:
   - What was tried before and why it failed
   - Working solutions we can reuse
   - Gotchas and warnings
   - Patterns or conventions established

4. **Deep dive selectively**: Only read full files if the snippet reveals something critical that needs more context.

5. **Report**: Briefly summarize what applies to the current task. If nothing relevant, say so and continue.

This avoids re-learning lessons the hard way or repeating failed approaches.
