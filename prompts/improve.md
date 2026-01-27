---
description: Suggest structural improvements to docs/agents organization
---
Review the current documentation structure and suggest up to 3 improvements:

1. **Audit current structure**:
   ```bash
   find docs/agents -type f -name "*.md" | head -30
   ```
   Note: file locations, naming patterns, folder organization

2. **Evaluate against usage patterns**:
   - Are autoloaded context files focused and minimal?
   - Are reference files easy to discover when needed?
   - Are handovers aging out properly to completed/?
   - Is there duplication across files?
   - Are deep dives worth their size, or could they be trimmed?

3. **Suggest up to 3 improvements** (if warranted):
   - Reorganize: split, merge, or move files
   - Rename: clearer naming conventions
   - New structure: missing categories or folders
   - Cleanup: stale content, redundant files

If the current structure is working well, say so. Don't suggest changes for the sake of changes.
