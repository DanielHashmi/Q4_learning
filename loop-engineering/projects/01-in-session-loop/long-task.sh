#!/bin/bash
# Simulates a long-running task (e.g., deployment, test suite, build process)

DURATION=${1:-180}  # Default 3 minutes, can be overridden
STATUS_FILE="task-status.txt"
RESULT_FILE="task-result.txt"

echo "⏳ Long task started at $(date)" > "$STATUS_FILE"
echo "Task will complete in approximately $DURATION seconds..."

# Simulate work with progress updates
for ((i=1; i<=5; i++)); do
    sleep $((DURATION / 5))
    echo "Progress: $((i * 20))% complete at $(date)" >> "$STATUS_FILE"
done

# Task completes successfully
echo "✅ Task completed successfully at $(date)" >> "$STATUS_FILE"
echo "Task finished at $(date). All systems operational." > "$RESULT_FILE"

echo "Task complete! Check task-result.txt for output."
