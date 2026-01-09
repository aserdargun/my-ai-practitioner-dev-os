# Learning Journal

This folder contains your weekly and monthly journal entries.

## Structure

```
journal/
├── README.md             # This file
├── weekly-template.md    # Template for weekly entries
├── monthly-template.md   # Template for monthly entries
└── YYYY-wWW.md          # Weekly entries (e.g., 2026-w01.md)
```

## Usage

### Creating Weekly Entries

**Option 1**: Use the hook

```bash
bash .claude/hooks/pre_week_start.sh
```

**Option 2**: Use the command

```
/start-week
```

**Option 3**: Manual

```bash
cp weekly-template.md 2026-w01.md
# Edit the file with your plan
```

### Writing in Your Journal

Each week, update your journal with:

1. **Goals** — What you plan to accomplish
2. **Daily Log** — Tasks completed each day
3. **Reflections** — What worked, what didn't
4. **Best Practices** — Insights to capture

### Completing Entries

At week's end:

```
/retro
```

Or run the hook:

```bash
bash .claude/hooks/post_week_review.sh
```

## Monthly Reviews

At the end of each month, create a monthly summary:

```bash
cp monthly-template.md 2026-m01.md
# Summarize the month
```

## Integration with Memory

Journal reflections inform:

- `/evaluate` — Measures reflection score
- `best_practices.md` — Insights are captured there
- `progress_log.jsonl` — Week completions are logged

## Tips

- Write brief daily notes (even 2-3 bullet points help)
- Be honest about challenges
- Capture insights immediately
- Review past entries before planning
