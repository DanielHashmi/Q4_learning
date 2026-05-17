MCQ 1: What is the tag name of built-in skills and extra skills?

1. bundled-skill for built-in, bundle-skill for extras.

2. native-skill for built-in, bundle-skill for extras.

3. OpenClaw-bundled for built-in, OpenClaw-bundle for extras.

4. OpenClaw-bundled for built-in, OpenClaw-extra for extras.

MCQ 2: What is the default tool profile?

1. Minimal.

2. Coding.

3. Messaging.

4. Inherit.

MCQ 3: I installed a plugin, both main and dani agent could access it, but when I updated SOUL.md file of main agent, it was isolated only for main, why?

1. because plugins are gateway level which are shared across agents, while SOUL.md is a workspace file so they are isolated per agent.

2. because plugins are gateway level which are isolated per agent, while SOUL.md is a workspace file so it's shared across agents.

3. because SOUL.md is a persona file so all agents inherit it, while plugins are capabilities which should be isolated per agent.

4. because plugins gives new capabilities so they should be shared, while SOUL.md is an identity file which should be isolated per agent.


MCQ 4: I was walking inside my uncle's room, the door was open, but I asked him before entering, what concept does this demonstrate related to openclaw gating?

1. It demonstrates the concept of tool profiles, like how the request have to ask the operator.

2. It demonstrates the concept of plugin hooks, like how the access is open or closed, binary.

3. It demonstrates the concept of plugin hooks, like how the operator is notified when a request arrives at the door.

4. It demonstrates the concept of nemoclaw, like how it sendboxes requests in an isolated environment.

MCQ 5: I configured an approval hook to ask me before executing any tool, but my openclaw employee executed context7 tools without asking me, why?

1. Hooks are not reliable enough for intercepting tool calls.

2. It depends on how strong your AI Model is, since hooks are executed by your configured AI Model.

3. Because hooks can't intercept MCP tools, you have to implement this yourself.

4. Because MCP tools bypass hooks, they need their own access control.

MCQ 6: I asked OpenClaw Employee to tell me was the tool call approval timed out or was denied, what will be the answer?

1. OpenClaw will answer "deny" because a team member denied the request.

2. Both are same to OpenClaw, because hooks don't provide metadata indicating why the tool was blocked.

3. OpenClaw will answer "timeout" because it was not approved within 120 seconds.

4. Both are same to OpenClaw, so it can't answer accurately.