---
name: task-monitor
description: Monitor the long-running task and report when it completes
---

# Task Monitor Skill

Check if the long-running task has finished by looking at the status files.

## How to check

1. Look for `task-result.txt` - if it exists, the task is DONE
2. If it doesn't exist yet, check `task-status.txt` for current progress, and stop checking until the next check time hits.
3. Report what you find in a clear, concise way and stop.

## What to report when DONE

When `task-result.txt` exists:
- Stop the loop yourself
- Say "✅ TASK COMPLETE!" clearly
- Show the contents of `task-result.txt`
- Show the final status from `task-status.txt`

## What to report when IN PROGRESS

When only `task-status.txt` exists:
- Say the task is still running
- Show the latest progress line
- Keep it brief - the user is not actively watching, and stop

## What to report when NOT STARTED

If neither file exists:
- Say the task hasn't been started yet
- Remind the user to run `bash long-task.sh` first
