---
description: Review session code changes for style and DRY
---
Review code created or modified this session for quality and consistency:

1. **Identify changes**:
   - List files modified this session (use git status/diff if available)
   - Focus on substantive code changes, not config or docs

2. **Style compliance**:
   - Before checking, identify which AGENTS.md section applies to each file
   - For JS: apply correct rules for client JS vs Node JS based on file location
   - Comment coverage: Is there a comment above almost every line?
   - Comment quality: Do comments explain intent, not syntax?
   - Single-line statements: short if/else/catch/etc on one line with comment above
   - Naming conventions, spacing, braces per language rules

3. **DRY check**:
   - Any repeated code blocks that could be consolidated?
   - Any patterns that appear multiple times that could be a helper function?

4. **Refactoring opportunities**:
   - Functions that could be improved, consolidated, or split
   - Only suggest if there's a clear win - don't refactor for refactoring's sake

5. **Propose fixes**:
   - List specific improvements with file:line references
   - Ask before making changes

$@
