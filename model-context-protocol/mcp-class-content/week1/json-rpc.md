# JSON-RPC #2

Is designed for triggering specific actions or functions called Remote Procedure Calls, means if our server has some functions, JSON-RPC is used to invoke them, a standard JSON-RPC request object has four main key-value pairs, the version "jsonrpc" and value usually "2.0", the method "method" which is the name of the action to take like "subtract", the parameters "params" to pass to that action as arguments like "[42, 23]" and ID "id" a unique identifier for this specific request so the server can send back a matching response, there are two type of requests, a standard Request which has an "id" to make sure the server be able to response back to the same "id", and a Notification which has no "id" since it doesn't expect a response back from the server, MCP strictly relies on JSON-RPC 2.0 version.

## Exercise

1. As of 2026 JSON-RPC 2.0 supports batching, mean the client can send an array of request objects in a single HTTP transaction

2. If "id" is present Standard Request, If "id" is not present Notification

3. A batch request may look like this: 
    ```
    [
        {
            "jsonrpc": "2.0",
            "method": "add",
            "params": [33, 35],
            "id": 1
        },
        {
            "jsonrpc": "2.0",
            "method": "subtract",
            "params": [42, 23],
            "id": 2
        }
    ]
    ```
4. Remote Procedure Calls are specific actions present on the server, which can be invoked by the client through JSON-RPC requests which contain the action name in "method" and it's arguments in "params".

5. REST was all about interacting with resources through HTTP, JSON-RPC is for executing actions on the server.

6. MCP official spec removed the support of batching in 2025-06-18 version, so it doesn't support batching anymore.

Good Luck👋🏻