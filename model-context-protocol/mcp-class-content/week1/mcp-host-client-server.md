# MCP Host, Client and Server #3

## Host

This is the Application like VS Code or ChatGPT.

## Client

This is a part inside Host, which translates the Request of the Host into JSON-RPC so that the Server understands it

## Server

This is the external program which holds the capabilities like Tools, Resources or Prompts which the Client can access

## Exercise

1. Tools: Executable actions or functions

2. Resources: Data or context that can be read (like a local file)

3. Prompts: Pre-written prompt templates

4. A Request from the Host can be made by a User which is called User-Controlled, an AI which is called Model-Controlled and the app itself which is called App-Controlled

5. Claude Code is the MCP Host, which uses the MCP Client to translate its Request into JSON-RPC so the MCP Server can understand it, This Request can be a Model-Controlled call to invoke a Tool, an App-Controlled call to read a Resource, OR a User-Controlled call to use a prompt template, this association is practical convention, not protocol binding

6. You can build your own custom MCP Server, Client and Host 

7. Primitives are Tools, Resources and Prompts and their controllers are Model, App and User

Good Luck👋🏻