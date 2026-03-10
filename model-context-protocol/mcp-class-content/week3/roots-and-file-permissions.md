# Roots and File Permissions #11

## Roots:

Roots define the specific locations the server is allowed to access. These locations can be folders, files, or URIs. Instead of allowing the server to read everything on the system, the client uses Roots to tell the server exactly which paths are approved. This creates a clear boundary: the server should only work with data inside those defined paths.

## File Permissions:

File permissions control what actions the server is allowed to perform inside those Roots. Even if a folder is listed as a Root, the server may still have limited abilities, such as reading files, writing files, or modifying files. These permissions tell the server what actions are explicitly allowed.

## Exercise:

1. Roots define where the server is allowed to access in the file system or URI space

2. File permissions define what the server is allowed to do inside those locations

3. **Crucial Rule:** Roots and permissions are informational, not enforced by the protocol itself

4. The MCP protocol will not magically stop a Python script from reading a file outside the Root folder

5. You, as the developer, must write the actual code inside your server to check these boundaries and block actions that go outside of them

6. Roots control the location, permissions control the actions, but your code enforces the lock

Good Luck!👋🏻