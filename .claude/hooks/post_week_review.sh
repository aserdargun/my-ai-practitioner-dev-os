#!/usr/bin/env bash

# Hook: post_week_review
# Description: Prompts retrospective and updates progress log after completing a week
# Usage: bash .claude/hooks/post_week_review.sh

set -euo pipefail

echo "=== Post-Week Review Hook ==="

# Get current week and year
WEEK_NUM=$(date +%V)
YEAR=$(date +%Y)

# Paths
JOURNAL_DIR="paths/Advanced/journal"
WEEK_FILE="$JOURNAL_DIR/${YEAR}-w${WEEK_NUM}.md"
PROGRESS_LOG=".claude/memory/progress_log.jsonl"
BEST_PRACTICES=".claude/memory/best_practices.md"

# Check if week journal exists
if [ ! -f "$WEEK_FILE" ]; then
    echo "Warning: Week journal not found: $WEEK_FILE"
    echo "Run pre_week_start.sh first or create the file manually."
fi

echo ""
echo "=== Retrospective Prompts ==="
echo ""
echo "Take a moment to reflect on this week. Answer these questions:"
echo ""
echo "1. What went well this week?"
echo "   - What accomplishments are you proud of?"
echo "   - What felt easy or enjoyable?"
echo ""
echo "2. What was challenging?"
echo "   - Where did you struggle?"
echo "   - What took longer than expected?"
echo ""
echo "3. What did you learn?"
echo "   - New technical knowledge?"
echo "   - About your learning process?"
echo ""
echo "4. What will you try differently next week?"
echo "   - Specific changes to your approach?"
echo "   - Habits to adjust?"
echo ""

# Prompt for completion status
echo "---"
echo ""
read -p "Did you complete your week's goals? (yes/partial/no): " COMPLETION_STATUS

# Prompt for highlights
echo ""
read -p "What was your main accomplishment? (one sentence): " HIGHLIGHT

# Log to progress log
if [ -f "$PROGRESS_LOG" ] || [ -d "$(dirname "$PROGRESS_LOG")" ]; then
    TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

    # Escape quotes in highlight
    HIGHLIGHT_ESCAPED=$(echo "$HIGHLIGHT" | sed 's/"/\\"/g')

    LOG_ENTRY="{\"timestamp\": \"$TIMESTAMP\", \"event\": \"week_complete\", \"week\": $WEEK_NUM, \"year\": $YEAR, \"status\": \"$COMPLETION_STATUS\", \"highlight\": \"$HIGHLIGHT_ESCAPED\"}"

    echo "$LOG_ENTRY" >> "$PROGRESS_LOG"
    echo ""
    echo "Logged week completion to: $PROGRESS_LOG"
else
    echo "Warning: Could not log to progress log (file not found)"
fi

# Prompt for best practices
echo ""
echo "---"
echo ""
read -p "Did you discover any best practices to capture? (yes/no): " HAS_BEST_PRACTICE

if [ "$HAS_BEST_PRACTICE" = "yes" ] || [ "$HAS_BEST_PRACTICE" = "y" ]; then
    echo ""
    echo "Great! Use the /add-best-practice command to capture it:"
    echo ""
    echo "  /add-best-practice — [describe your insight here]"
    echo ""
    echo "Or manually append to: $BEST_PRACTICES"
fi

echo ""
echo "=== Week $WEEK_NUM Review Complete ==="
echo ""
echo "Next steps:"
echo "  1. Update your journal: $WEEK_FILE"
echo "  2. Fill in the Reflections section"
echo "  3. Run /evaluate to see your progress scores"
echo "  4. Run /plan-week for next week"
echo ""
