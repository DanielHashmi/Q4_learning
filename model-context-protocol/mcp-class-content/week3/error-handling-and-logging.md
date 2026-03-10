# Error Handling and Recovery #13

## Error Handling:

Error Handling is simply how the server catches mistakes without dying. It's the built-in way to deal with bad inputs, missing files, or broken background links. Instead of just freezing, the server uses standard error codes to tell the client exactly what went wrong so the AI knows why its request failed.

## Recovery:

Recovery is how the server bounces back to keep working. It's actually a safety net that ensures one broken task does not destroy the entire system. It introduces a simple rule: catch the error, report the failure, and immediately go back to waiting for the next command.

## Exercise:

1. To explain a failure to the AI: Use Error Handling with standard error codes

2. To keep the server alive after a failure: Use Recovery patterns

3. If a tool cannot find a database, it must send an error message back instead of crashing the whole process

4. NOTE: Error Handling explains the problem, Recovery survives the problem

5. The server must isolate errors so one bad tool call does not break the other tools

6. No error handling means silent crashes and broken AI agents

Good Luck!👋🏻