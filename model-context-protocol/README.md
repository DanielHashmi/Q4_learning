# 🔌 Model Context Protocol (MCP)

![MCP Image](main.png)

This repository contains a comprehensive 3-week learning curriculum for **Model Context Protocol (MCP)**, a universal standard for connecting AI applications with custom data and tools.

---

## 📚 Curriculum Overview

This progresses from foundational concepts to production-ready implementations:

### **Week 1: Foundations** 
*Learn the core concepts and architecture of MCP*

- [basic-mcp-server.md](mcp-class-content/week1/basic-mcp-server.md) - Introduction to basic MCP servers
- [json-rpc.md](mcp-class-content/week1/json-rpc.md) - JSON-RPC protocol fundamentals
- [http-and-rest.md](mcp-class-content/week1/http-and-rest.md) - HTTP/REST concepts
- [mcp-host-client-server.md](mcp-class-content/week1/mcp-host-client-server.md) - MCP architecture overview
- [mcp_server.py](mcp-class-content/week1/mcp_server.py) - Basic server implementation example

### **Week 2: Extending MCP Servers**
*Build servers with Resources, Prompts, and Streamable protocols*

- [resources-and-prompts.md](mcp-class-content/week2/resources-and-prompts.md) - Core MCP concepts: Resources and Prompts
- [extend-mcp-server.md](mcp-class-content/week2/extend-mcp-server.md) - How to extend basic servers
- [stdio-and-streamable.md](mcp-class-content/week2/stdio-and-streamable.md) - Transport protocols
- [extend_mcp_server_with_resource.py](mcp-class-content/week2/extend_mcp_server_with_resource.py) - Adding resources to servers
- [extend_mcp_server_with_prompt.py](mcp-class-content/week2/extend_mcp_server_with_prompt.py) - Adding prompts to servers
- [full_extended_server.py](mcp-class-content/week2/full_extended_server.py) - Complete extended server example
- [mcp_server_with_streamable.py](mcp-class-content/week2/mcp_server_with_streamable.py) - Streamable protocol implementation

### **Week 3: Production & Advanced Topics**
*Master advanced features and deploy production-ready servers*

**Core Topics:**
- [error-handling-and-logging.md](mcp-class-content/week3/error-handling-and-logging.md) - Error handling strategies
- [logging-notifications.md](mcp-class-content/week3/logging-notifications.md) - Logging and server notifications
- [context-object-and-lifespan.md](mcp-class-content/week3/context-object-and-lifespan.md) - Server lifecycle management
- [stateful-and-stateless.md](mcp-class-content/week3/stateful-and-stateless.md) - Server state management
- [security-and-oauth.md](mcp-class-content/week3/security-and-oauth.md) - Security best practices and OAuth
- [http-vs-https.md](mcp-class-content/week3/http-vs-https.md) - HTTP vs HTTPS considerations
- [roots-and-file-permissions.md](mcp-class-content/week3/roots-and-file-permissions.md) - File system access and permissions
- [sampling-and-elicitation.md](mcp-class-content/week3/sampling-and-elicitation.md) - Advanced MCP patterns

**Implementation Examples:**
- [basic_mcp_and_agent/](mcp-class-content/week3/basic_mcp_and_agent/) - Basic MCP server with agent integration
- [production_mcp_and_agent/](mcp-class-content/week3/production_mcp_and_agent/) - Production-ready implementations
  - [server_stdio.py](mcp-class-content/week3/production_mcp_and_agent/server_stdio.py) - Stdio transport implementation
  - [server_streamable_http.py](mcp-class-content/week3/production_mcp_and_agent/server_streamable_http.py) - HTTP streamable transport
  - [client_stdio.py](mcp-class-content/week3/production_mcp_and_agent/client_stdio.py) - Stdio client example
  - [client_streamable_http.py](mcp-class-content/week3/production_mcp_and_agent/client_streamable_http.py) - HTTP streamable client example
  - [sampling_elicitation_and_roots.py](mcp-class-content/week3/production_mcp_and_agent/sampling_elicitation_and_roots.py) - Advanced patterns: LLM sampling, human elicitation, and filesystem roots

---

## 🎯 What is MCP?

MCP is a universal standard that allows:
- 🤖 **AI applications** to access external data and tools
- 🖥️ **MCP servers** to expose Resources, Prompts, and Tools
- 🔗 **MCP clients** to manage connections between applications and servers

---

## 🧱 Core Concepts

MCP servers provide three primary building blocks:

| Building Block | Description |
|----------------|-------------|
| 📦 **Resources** | Data and information (files, database records, API responses) |
| 💬 **Prompts** | Pre-built templates to guide AI conversations |
| 🔧 **Tools** | Actions the AI can invoke (search, create, call APIs) |

---

## 🚀 How to Use This Repository

1. **Start with Week 1** if you're new to MCP - understand the fundamentals
2. **Progress to Week 2** to build your first extended servers
3. **Complete Week 3** to master production patterns and deployment
4. Each markdown file explains concepts; Python files provide working examples
5. Refer to the `README.md` files in Week 3's project folders for practical setup instructions

Keep building! 🎗️