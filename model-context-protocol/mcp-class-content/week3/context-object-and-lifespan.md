# Context Object and Lifespan #8

## Context Object:

Context Object is the server’s **internal memory for one running task**.
When an MCP server receives a request from a client, it starts doing work for that request. While doing that work, the server must remember things like the current step, temporary data, or results produced so far.

The Context Object stores this **temporary working state** so the server does not lose track of what it is doing. It keeps the information needed while the request is being processed.

When the task finishes, that Context Object is no longer needed.

## Lifespan:

Lifespan manages the server’s **long-lived resources**, such as database connections or API clients.

While the Context Object handles the memory of the current task, Lifespan handles the **setup and shutdown of shared resources** that the server needs to perform those tasks.

It makes sure that these external connections:

* open when the server starts
* stay available while the server is running
* close safely when the server shuts down

## Exercise:

1. If your server opens a **brand new internet connection** for every request, it is slow and wasteful. It is like buying a new phone every time you want to make a call and then throwing it away.
   MCP Lifespan keeps one phone available for the entire time the server is running, so it can be used for many calls

2. If you **do not pass `lifespan` to FastMCP**, your tools still work, but they do not share resources. Every tool call runs independently, with no shared state or connections

3. For external services, place things like **database connections and API clients inside the Lifespan rules**

4. The **Context Object handles internal task state**, while **Lifespan manages external resources**

5. Context manages **temporary memory**, and Lifespan manages **persistent connections**

6. Without lifespan management, database connections may remain open and unused, which can eventually break the server


## Usage Scenario: Support Ticket Server

### The Setup

Consider an MCP server used to manage IT support tickets.

When the server starts, the **Lifespan manager** opens a connection to the company’s ticket database and keeps that connection available while the server is running.

### The Action

A user sends the prompt:

**"Mark ticket #404 as resolved."**

The server triggers the `update_ticket` tool.

The tool needs database access. It checks the **Context Object**, where it can access the database connection that Lifespan created. Using that connection, it updates the ticket status.

### The Shutdown

When the server stops running, the **Lifespan manager closes the database connection** so no unused or broken connections remain.

Good Luck!👋🏻
