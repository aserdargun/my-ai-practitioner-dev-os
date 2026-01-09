#!/usr/bin/env bash

# Hook: pre_week_start
# Description: Creates week plan stub and updates tracker before starting a new week
# Usage: bash .claude/hooks/pre_week_start.sh

set -euo pipefail

echo "=== Pre-Week Start Hook ==="

# Get current week and year
WEEK_NUM=$(date +%V)
YEAR=$(date +%Y)
DATE=$(date +%Y-%m-%d)

# Paths
JOURNAL_DIR="paths/Advanced/journal"
TEMPLATE="$JOURNAL_DIR/weekly-template.md"
WEEK_FILE="$JOURNAL_DIR/${YEAR}-w${WEEK_NUM}.md"
TRACKER="paths/Advanced/tracker.md"
PROGRESS_LOG=".claude/memory/progress_log.jsonl"

# Check if journal directory exists
if [ ! -d "$JOURNAL_DIR" ]; then
    echo "Creating journal directory..."
    mkdir -p "$JOURNAL_DIR"
fi

# Create week journal entry if it doesn't exist
if [ -f "$WEEK_FILE" ]; then
    echo "Week journal already exists: $WEEK_FILE"
else
    if [ -f "$TEMPLATE" ]; then
        echo "Creating week journal from template..."
        cp "$TEMPLATE" "$WEEK_FILE"
        # Replace placeholders
        sed -i "s/{{WEEK_NUMBER}}/$WEEK_NUM/g" "$WEEK_FILE" 2>/dev/null || \
        sed -i '' "s/{{WEEK_NUMBER}}/$WEEK_NUM/g" "$WEEK_FILE"
        sed -i "s/{{YEAR}}/$YEAR/g" "$WEEK_FILE" 2>/dev/null || \
        sed -i '' "s/{{YEAR}}/$YEAR/g" "$WEEK_FILE"
        sed -i "s/{{DATE}}/$DATE/g" "$WEEK_FILE" 2>/dev/null || \
        sed -i '' "s/{{DATE}}/$DATE/g" "$WEEK_FILE"
        echo "Created: $WEEK_FILE"
    else
        echo "Template not found, creating minimal journal entry..."
        cat > "$WEEK_FILE" << EOF
# Week $WEEK_NUM — $YEAR

**Date**: $DATE

## Goals
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

## Daily Log

### Monday
- [ ] Task 1

### Tuesday
- [ ] Task 1

### Wednesday
- [ ] Task 1

### Thursday
- [ ] Task 1

### Friday
- [ ] Task 1

## Reflections
(To be filled during /retro)

## Best Practices Discovered
(To be added to .claude/memory/best_practices.md)
EOF
        echo "Created: $WEEK_FILE"
    fi
fi

# Update progress log
if [ -f "$PROGRESS_LOG" ]; then
    echo "Logging week start..."
    TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    echo "{\"timestamp\": \"$TIMESTAMP\", \"event\": \"week_start\", \"week\": $WEEK_NUM, \"year\": $YEAR}" >> "$PROGRESS_LOG"
    echo "Logged to: $PROGRESS_LOG"
else
    echo "Progress log not found: $PROGRESS_LOG"
    echo "Creating progress log..."
    mkdir -p "$(dirname "$PROGRESS_LOG")"
    TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    echo "{\"timestamp\": \"$TIMESTAMP\", \"event\": \"week_start\", \"week\": $WEEK_NUM, \"year\": $YEAR}" > "$PROGRESS_LOG"
fi

echo ""
echo "=== Week $WEEK_NUM Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Review your week journal: $WEEK_FILE"
echo "  2. Fill in your goals for the week"
echo "  3. Run /plan-week for detailed planning"
echo ""
