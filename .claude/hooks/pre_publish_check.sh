#!/usr/bin/env bash

# Hook: pre_publish_check
# Description: Runs tests, lints, and checks docs before publishing
# Usage: bash .claude/hooks/pre_publish_check.sh

set -euo pipefail

echo "=== Pre-Publish Check Hook ==="
echo ""

# Track overall status
CHECKS_PASSED=0
CHECKS_FAILED=0

# Function to report check result
report_check() {
    local name=$1
    local status=$2
    if [ "$status" -eq 0 ]; then
        echo "  ✓ $name"
        ((CHECKS_PASSED++))
    else
        echo "  ✗ $name"
        ((CHECKS_FAILED++))
    fi
}

echo "Running checks..."
echo ""

# Check 1: Python tests (if pytest is available)
echo "1. Running tests..."
if command -v pytest &> /dev/null; then
    if pytest --tb=short -q 2>/dev/null; then
        report_check "Tests passing" 0
    else
        report_check "Tests passing" 1
    fi
else
    echo "  - pytest not found, skipping tests"
fi

# Check 2: Linting (if ruff is available)
echo ""
echo "2. Running linter..."
if command -v ruff &> /dev/null; then
    if ruff check . --quiet 2>/dev/null; then
        report_check "Linting clean" 0
    else
        report_check "Linting clean" 1
        echo "    Run 'ruff check .' to see issues"
    fi
else
    echo "  - ruff not found, skipping lint"
fi

# Check 3: No secrets in common files
echo ""
echo "3. Checking for potential secrets..."
SECRETS_FOUND=0

# Check for common secret patterns
if grep -r "api_key\s*=\s*['\"][^'\"]\+" --include="*.py" --include="*.md" . 2>/dev/null | grep -v ".env" | grep -v "example" | head -5; then
    SECRETS_FOUND=1
fi

if grep -r "password\s*=\s*['\"][^'\"]\+" --include="*.py" . 2>/dev/null | grep -v ".env" | grep -v "example" | head -5; then
    SECRETS_FOUND=1
fi

if [ $SECRETS_FOUND -eq 0 ]; then
    report_check "No obvious secrets" 0
else
    report_check "No obvious secrets" 1
    echo "    Review the above matches for potential secrets"
fi

# Check 4: README exists and has content
echo ""
echo "4. Checking documentation..."
if [ -f "README.md" ] && [ -s "README.md" ]; then
    report_check "README.md exists" 0
else
    report_check "README.md exists" 1
fi

# Check 5: Check for TODO/FIXME in code
echo ""
echo "5. Checking for TODO/FIXME comments..."
TODO_COUNT=$(grep -r "TODO\|FIXME" --include="*.py" . 2>/dev/null | wc -l | tr -d ' ')
if [ "$TODO_COUNT" -eq 0 ]; then
    report_check "No TODO/FIXME comments" 0
else
    echo "  - Found $TODO_COUNT TODO/FIXME comments (not blocking)"
    report_check "No TODO/FIXME comments" 0
fi

# Check 6: Git status
echo ""
echo "6. Checking git status..."
if command -v git &> /dev/null; then
    UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    if [ "$UNCOMMITTED" -eq 0 ]; then
        report_check "No uncommitted changes" 0
    else
        echo "  - Found $UNCOMMITTED uncommitted changes"
        report_check "No uncommitted changes" 1
    fi
else
    echo "  - git not found, skipping"
fi

# Summary
echo ""
echo "=== Summary ==="
echo ""
echo "Checks passed: $CHECKS_PASSED"
echo "Checks failed: $CHECKS_FAILED"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo "✓ All checks passed! Ready to publish."
    exit 0
else
    echo "✗ Some checks failed. Review above and fix before publishing."
    exit 1
fi
