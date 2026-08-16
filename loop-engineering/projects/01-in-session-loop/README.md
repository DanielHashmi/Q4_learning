# Project 1: In-Session Loop Monitor

**Difficulty:** Easy  
**Concept:** Concept 4 - In-session loops (repeat while you watch)

## What This Demonstrates

This project shows you how to use Claude's `/loop` feature to monitor a long-running task without sitting and watching it. The loop checks every minute whether your task has finished and tells you the moment it completes.

## The Scenario

You start a long-running task (simulated by `long-task.sh` - imagine it's a deployment, test suite, or build process). Instead of watching the terminal or checking back every few minutes, you set up an in-session loop that monitors it for you and reports when it's done.

## Project Structure

```
01-in-session-loop/
├── README.md           # This file
├── long-task.sh        # Simulates a long-running task (3 minutes by default)
```

## How to Use This Project

### Step 1: Navigate to this folder

```bash
cd projects/01-in-session-loop
```

### Step 2: Start the long-running task in the background

```bash
bash long-task.sh
```

This starts a task that will run for about 3 minutes (you can customize the duration: `bash long-task.sh 300` for 5 minutes).

The task creates two files:
- `task-status.txt` - updates with progress during execution
- `task-result.txt` - created only when the task completes

### Step 3: Start the monitoring loop

In your Claude session, type:

```
/loop 1m check if the long task has finished using the task-monitor-skill
```

This tells Claude to:
- Check every 1 minute (you can use `30s` for 30 seconds, `2m` for 2 minutes, etc.)
- Use the `.claude/skills/task-monitor-skill/SKILL.md` to check the task status
- Report back each time it checks

### Step 4: Go do something else

The key insight: **you don't have to watch the terminal**. Claude will check every minute and tell you when it's done.

### Step 5: See it detect completion

When the task finishes (after ~3 minutes), Claude's next check will see `task-result.txt` and report:

```
✅ TASK COMPLETE!
```

### Step 6: Stop the monitoring loop

After the task completes, the loop will continue checking every minute until you explicitly tell claude to stop it, close the session or it reaches it's expiry. The loop doesn't automatically stop when it detects completion.

To stop the loop, simply tell Claude in natural language:

```
stop the loop
```

Claude will use the `CronDelete` tool internally to cancel the scheduled checks.

## What You're Learning

This demonstrates the core concept of an **in-session loop**:

1. **It repeats automatically** - You don't manually type "check status" every minute
2. **It runs while the session is open** - Close the terminal and the loop stops
3. **It reports at key moments** - You get notified when something changes
4. **It's cleanly cancelable** - You stop it when done

**Done when:** The loop notices the task finished, reports it once clearly, and you can stop it without any lingering processes.