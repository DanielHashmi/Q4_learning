# HTTP vs. HTTPS #14

## HTTP:

HTTP sends data exactly as it is written. It means every single message passed between the client and the server is in plain text. If a hacker is watching the network, they can easily read everything you send, including passwords or sensitive data.

## HTTPS:

HTTPS is HTTP with a lock. The "S" stands for Secure. It encrypts the data before sending it over the network. It introduces a strict rule: all messages are scrambled into unreadable, chaotic code while traveling. Even if someone intercepts the connection, the data is completely useless to them because they do not have the key to unscramble it.

## Exercise:

1. To send basic, non-sensitive text: HTTP used to be acceptable

2. To send login codes, user data, or API keys: HTTPS is absolutely required

3. The encryption scrambles the data in transit

4. NOTE: OAuth 2.1 passes secret authorization tokens back and forth to log users in

5. If you send OAuth 2.1 tokens over plain HTTP, anyone watching the network can steal those tokens and impersonate the user

6. No HTTPS means stolen data and an immediately rejected MCP connection

Good Luck!👋🏻