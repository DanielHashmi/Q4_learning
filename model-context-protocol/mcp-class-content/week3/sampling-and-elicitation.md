# Sampling and Elicitation #10

## Sampling:

Sampling is when the **server asks the AI model for help**.

If the MCP server needs the model to **analyze information, generate text, or make a decision**, it sends a request upward to the LLM. The request goes from the **server → client → LLM**, and the result comes back **LLM → client → server**.

This allows the server to use the model’s intelligence during its work.

## Elicitation:

Elicitation is when the **server pauses and asks the human user for input**.

Instead of asking the AI, the server sends a structured request to the client so the **user can provide a specific answer directly**. The answer must be a **simple data value**, such as text, number, or a basic selection.

There is also a strict rule: **Elicitation must never request sensitive personal information or PII.**

## Exercise:

1. To have the AI **evaluate, analyze, or generate something automatically**, use **Sampling**

2. To ask the **human user a direct question** (for example a preference or confirmation), use **Elicitation**

3. Sampling works through the **client’s connection to the LLM**, which allows the server to receive a model-generated response

4. Elicitation sends a request to the **user interface**, and the response must be a **simple value such as text, number, or selection**

5. **Never use Elicitation to ask for passwords, credit cards, or personal information**

6. Simple rule: **Sampling asks the AI, Elicitation asks the human**

Good Luck!👋🏻
