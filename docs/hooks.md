# Hooks Guide

Automation scripts for your learning workflow.

---

## Overview

Hooks are shell scripts that automate common tasks at specific points:

| Hook | Trigger | Purpose |
|------|---------|---------|
| `pre_week_start.sh` | Before starting a week | Create journal, update tracker |
| `post_week_review.sh` | After completing a week | Prompt retro, log completion |
| `pre_publish_check.sh` | Before publishing | Run tests, lint, check docs |

---

## Running Hooks

### From Repository Root

```bash
bash .claude/hooks/pre_week_start.sh
bash .claude/hooks/post_week_review.sh
bash .claude/hooks/pre_publish_check.sh
```

### Through Commands

Commands may invoke hooks (with your approval):

- `/start-week` can run `pre_week_start.sh`
- `/retro` can run `post_week_review.sh`
- `/publish` can run `pre_publish_check.sh`

---

## Cross-Platform Compatibility

These hooks are shell scripts intended for:

- **Linux**: Native bash
- **macOS**: Native bash
- **Windows**: WSL (recommended) or Git Bash

### Windows Setup

#### Option 1: WSL (Recommended)

1. Open PowerShell as Administrator
2. Run: `wsl --install`
3. Restart your computer
4. Open WSL terminal
5. Navigate to your repo
6. Run scripts normally

#### Option 2: Git Bash

1. Install [Git for Windows](https://git-scm.com/download/win)
2. Open Git Bash
3. Navigate to your repo
4. Run scripts normally

---

## Hook Details

### pre_week_start.sh

**Purpose**: Set up a new week with journal and tracker updates.

**What it does**:
1. Creates week journal entry from template
2. Replaces date placeholders
3. Logs week start to progress log
4. Shows next steps

**Usage**:
```bash
bash .claude/hooks/pre_week_start.sh
```

**Output**:
```
=== Pre-Week Start Hook ===
Creating week journal from template...
Created: paths/Advanced/journal/2026-w03.md
Logged to: .claude/memory/progress_log.jsonl

=== Week 3 Setup Complete ===

Next steps:
  1. Review your week journal
  2. Fill in your goals
  3. Run /plan-week for detailed planning
```

### post_week_review.sh

**Purpose**: Facilitate reflection and log week completion.

**What it does**:
1. Displays reflection prompts
2. Asks for completion status
3. Captures week highlight
4. Logs to progress log
5. Prompts for best practices

**Usage**:
```bash
bash .claude/hooks/post_week_review.sh
```

**Interactive prompts**:
```
Did you complete your week's goals? (yes/partial/no): partial
What was your main accomplishment? Finished embedding pipeline
Did you discover any best practices to capture? yes
```

### pre_publish_check.sh

**Purpose**: Verify quality before publishing.

**What it does**:
1. Runs pytest (if available)
2. Runs ruff linter (if available)
3. Checks for potential secrets
4. Verifies README exists
5. Checks for TODOs
6. Reports git status

**Usage**:
```bash
bash .claude/hooks/pre_publish_check.sh
```

**Output**:
```
=== Pre-Publish Check Hook ===

Running checks...

1. Running tests...
  ✓ Tests passing

2. Running linter...
  ✓ Linting clean

3. Checking for potential secrets...
  ✓ No obvious secrets

4. Checking documentation...
  ✓ README.md exists

5. Checking for TODO/FIXME comments...
  - Found 3 TODO/FIXME comments (not blocking)

6. Checking git status...
  ✓ No uncommitted changes

=== Summary ===

Checks passed: 5
Checks failed: 0

✓ All checks passed! Ready to publish.
```

---

## Manual Fallback

If you cannot run `.sh` scripts, here are the equivalent steps:

### pre_week_start.sh — Manual

1. Copy the weekly template:
   ```
   cp paths/Advanced/journal/weekly-template.md paths/Advanced/journal/2026-wXX.md
   ```

2. Edit the new file:
   - Replace `{{WEEK_NUMBER}}` with current week
   - Replace `{{DATE}}` with current date

3. Add to progress log:
   ```bash
   echo '{"timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'", "event": "week_start", "week": XX}' >> .claude/memory/progress_log.jsonl
   ```

### post_week_review.sh — Manual

1. Open your week's journal file
2. Fill in the Reflections section
3. Add to progress log:
   ```bash
   echo '{"timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'", "event": "week_complete", "week": XX, "status": "complete"}' >> .claude/memory/progress_log.jsonl
   ```

### pre_publish_check.sh — Manual

Run these commands:

```bash
# 1. Run tests
pytest

# 2. Run linter
ruff check .

# 3. Check for secrets (manual review)
grep -r "api_key\|password\|secret" --include="*.py" .

# 4. Verify README
cat README.md | head -5

# 5. Check TODOs
grep -r "TODO\|FIXME" --include="*.py" . | wc -l

# 6. Git status
git status
```

---

## Creating New Hooks

To add a new hook:

1. Create `.claude/hooks/your_hook.sh`
2. Add the shebang: `#!/usr/bin/env bash`
3. Make it executable: `chmod +x your_hook.sh`
4. Use `set -euo pipefail` for safety
5. Update this document

### Template

```bash
#!/usr/bin/env bash

# Hook: your_hook_name
# Description: What this hook does
# Usage: bash .claude/hooks/your_hook.sh

set -euo pipefail

echo "=== Your Hook Name ==="

# Your automation logic here

echo "Done!"
```

---

## Troubleshooting

### "Permission denied"

Make the script executable:
```bash
chmod +x .claude/hooks/pre_week_start.sh
```

### "Command not found: bash"

On Windows, use WSL or Git Bash.

### "sed: illegal option"

macOS sed differs from GNU sed. The scripts handle this, but if issues persist, use the manual fallback.

### Script seems to hang

Some hooks have interactive prompts. Check if they're waiting for input.

---

## Links

- [Hook files](../.claude/hooks/)
- [Memory system](memory-system.md)
- [Commands guide](commands.md)
