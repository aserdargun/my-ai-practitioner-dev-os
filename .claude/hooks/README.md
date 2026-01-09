# Hooks

This folder contains automation scripts that run at specific points in your learning workflow.

## Overview

Hooks are shell scripts that automate common tasks:

| Hook | Trigger | Purpose |
|------|---------|---------|
| [pre_week_start.sh](pre_week_start.sh) | Before starting a week | Create week plan stub, update tracker |
| [post_week_review.sh](post_week_review.sh) | After completing a week | Prompt retrospective, update progress log |
| [pre_publish_check.sh](pre_publish_check.sh) | Before publishing | Run tests, lint, check docs |

## Usage

### Running Hooks Manually

```bash
# From repository root
bash .claude/hooks/pre_week_start.sh
bash .claude/hooks/post_week_review.sh
bash .claude/hooks/pre_publish_check.sh
```

### With Commands

Commands may invoke hooks automatically (with your approval):

- `/start-week` can run `pre_week_start.sh`
- `/retro` can run `post_week_review.sh`
- `/publish` can run `pre_publish_check.sh`

## Cross-Platform Compatibility

These hooks are shell scripts intended for:
- **Linux**: Native bash
- **macOS**: Native bash
- **Windows**: WSL (recommended) or Git Bash

### Windows Setup

#### Option 1: WSL (Recommended)
1. Install WSL: `wsl --install`
2. Open WSL terminal
3. Navigate to your repo
4. Run scripts normally

#### Option 2: Git Bash
1. Install Git for Windows (includes Git Bash)
2. Open Git Bash
3. Navigate to your repo
4. Run scripts normally

## Manual Fallback

If you cannot run `.sh` scripts, here are the equivalent manual steps:

### pre_week_start.sh — Manual Steps

```bash
# 1. Create week journal entry
WEEK_NUM=$(date +%V)
YEAR=$(date +%Y)
JOURNAL_FILE="paths/Advanced/journal/${YEAR}-w${WEEK_NUM}.md"

# 2. Copy template
cp paths/Advanced/journal/weekly-template.md "$JOURNAL_FILE"

# 3. Update date in file
# Edit the file to add current date

# 4. Update tracker
# Edit paths/Advanced/tracker.md to point to current week
```

### post_week_review.sh — Manual Steps

```bash
# 1. Open your week's journal entry
# paths/Advanced/journal/YYYY-wWW.md

# 2. Fill in the Reflections section

# 3. Add entry to progress log
# Append to .claude/memory/progress_log.jsonl:
echo '{"timestamp": "'$(date -Iseconds)'", "event": "week_complete", "week": '$(date +%V)'}' >> .claude/memory/progress_log.jsonl
```

### pre_publish_check.sh — Manual Steps

```bash
# 1. Run tests
pytest

# 2. Run linter
ruff check .

# 3. Check for broken links (if you have a link checker)
# Or manually verify links in README

# 4. Verify docs are up to date
# Check that README reflects current state
```

## Creating New Hooks

To add a new hook:

1. Create a new `.sh` file in this folder
2. Add the shebang: `#!/usr/bin/env bash`
3. Make it executable: `chmod +x your_hook.sh`
4. Update this README
5. Update `docs/hooks.md`

## Hook Template

```bash
#!/usr/bin/env bash

# Hook: your_hook_name
# Description: What this hook does
# Usage: bash .claude/hooks/your_hook.sh

set -euo pipefail

echo "Running your_hook..."

# Your automation logic here

echo "Done!"
```
