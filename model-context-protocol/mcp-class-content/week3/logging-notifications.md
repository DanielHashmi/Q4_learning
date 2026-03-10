# Progress and Logging Notifications #9

## Logging:

Logging is how the **server reports its internal status to the client**.

The server sends messages (`notifications/message`) that describe what is happening inside the system. These messages include **information, warnings, or errors**, and each message has a severity level.

This allows developers or monitoring systems to **observe the server’s behavior and detect problems early**

## Progress:

Progress is how the **server reports the advancement of a long-running task**.

Instead of remaining silent during heavy work, the server sends updates (`notifications/progress`) that include:

* a `progressToken` to identify the task
* the current `progress` value
* the `total` expected amount of work

The client application can use this information to **display a progress indicator** so the user knows the task is still running

## Exercise:

1. If a server processes a large file for several minutes without any updates, the user may think it stopped working.
   Progress notifications send updates (for example **"step 2 of 10"**) so the client can display a loading or progress bar

2. If Logging is not used, failures become difficult to diagnose.
   Logging allows the server to report issues such as **"Warning: Database connection is slow"** before a larger failure occurs

3. To monitor system behavior, warnings, and errors: use **Logging notifications** with `logging/setLevel`

4. To report the advancement of long-running tasks: use **Progress notifications** with a token, current value, and total value

5. Logging is mainly for **developers and system monitoring**, while Progress is mainly for **user feedback during long tasks**

6. Without progress updates, users may assume the system is frozen or broken

## Usage Scenario: Data Analysis Server

### The Setup

Consider an MCP server designed to analyze large spreadsheet files.

A user sends a request:
**"Find the sales trends for the last 10 years."**

The server starts a heavy analysis that will take several minutes

### The Action (Progress)

While the analysis runs, the server sends **Progress notifications** such as:

* `progress: 500`
* `total: 1000`

The client interface uses these values to show a loading bar like **"Analyzing Data..."**, letting the user know the task is progressing

### The Action (Logging)

During processing, the server finds a corrupted row in the spreadsheet. The analysis continues, but the server sends a **Logging notification** with a **Warning** level message so developers know that the data contained an issue.

The user receives the final analysis without thinking the system stopped working, and developers receive a clear log describing the corrupted data.

Good Luck!👋🏻
