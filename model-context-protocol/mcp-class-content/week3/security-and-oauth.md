# Security and OAuth 2.1 #15

## Security:
MCP servers handle sensitive user data, so security is taken very seriously. The connection between the client and the server must always use HTTPS ,  a secure, encrypted channel. Sending data over regular, unencrypted HTTP is not allowed under any circumstances, because it would leave all messages exposed and readable by anyone who intercepts them

## OAuth 2.1:
OAuth 2.1 is the authorization system that controls who is allowed to access your MCP server. Think of it as a secure gatekeeper. The MCP client (your AI application) is the one asking for access, while the MCP server is the one deciding whether to grant it. To keep the login process safe, OAuth 2.1 requires a security mechanism called PKCE (Proof Key for Code Exchange). PKCE makes sure that the temporary code used during login cannot be stolen and used by an attacker

## Exercise:
1. Encrypt all communication: Always use HTTPS to protect data in transit

2. Manage access with OAuth 2.1: This is the required system for handling user login and permissions

3. Protect the login process: PKCE is mandatory ,  it prevents attackers from hijacking the authorization code during the login handshake

4. Know the roles: The MCP client is the OAuth 2.1 client; the MCP server is the OAuth 2.1 resource server

5. No shortcuts during testing: HTTPS is required even when testing locally ,  there are no exceptions

6. Follow the rules or be rejected: If either HTTPS or PKCE is missing, the MCP protocol will reject the connection

Good luck!👋🏻