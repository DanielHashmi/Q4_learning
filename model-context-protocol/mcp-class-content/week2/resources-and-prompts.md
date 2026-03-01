# Resources and Prompts #5

## Resources:

So! Resources are MCP's way of letting a server share data with a client, things like files, markdowns, or any application-specific information, every single resource is uniquely identified by a URI, like file:///project/src/main.rs. The control model is application-driven, meaning the host application decides how resources get selected and injected into context, it could show the user a picker, auto-include them silently, or use AI-driven heuristics, the protocol doesn't care which strategy the app uses. On the protocol level there are four key operations, first is resources/list to discover what's available, second is resources/read to actually fetch a resource's contents by URI, third is resources/templates/list for parameterized resources where the URI has variables like file:///{path} that get filled in at request time, and fourth is resources/subscribe which lets a client watch a specific resource and get notified via notifications/resources/updated whenever it changes. Resource contents come in two forms, either plain text or base64-encoded binary

## Prompts:

Are reusable prompt templates servers expose to clients. They accept arguments to customize output and are user-controlled — the user explicitly selects and triggers them. Slash commands are the classic UI example, but the protocol doesn't mandate any specific interaction pattern


## Exercise

1. Prompts are user-controlled because they are essentially pre-built conversation starters with named arguments a human can naturally fill in. The structure assumes a human is picking a template and customizing it

2. Resources are app-controlled because they carry metadata which is specifically useful for an application making automated decisions about what context to include

3. Imagine a coding assistant app. A file main.py is currently injected into the AI's context. The developer edits that file. The server fires notifications/resources/updated for that URI. The app silently re-fetches the updated content via resources/read and swaps it in the context. all without the user doing anything. The AI is now working with the latest version of the file without the user having to manually refresh or reselect anything, that is a completely automated background operation driven by the app. A human didn't trigger it, and the AI didn't decide to trigger it either. The app just maintained fresh context on its own

4. Imagine a coding assistant app. The developer selects a messy Python function and types /code-review in the chat. That slash command is an MCP Prompt registered on the server. The app calls prompts/get, passing the selected code as the code argument. The server returns a fully constructed messages array, the user's code is already baked into a well-crafted review request, and the app sends that straight to the LLM. The LLM replies with a detailed review. The developer didn't write the prompt themselves, and the app didn't have to hardcode any prompt logic. The server owned the template, the user just filled in the blank and pulled the trigger

5. Prompts are pre-made templates used with full intent and consciousness of User, while Resources can be handled by the App automatically, the fact that users CAN manually pick resources and apps CAN auto-fire prompts doesn't eliminate this distinction, it just means the convention isn't always followed

6. Prompts capture what to do, Resources capture what to know

Good Luck👋🏻