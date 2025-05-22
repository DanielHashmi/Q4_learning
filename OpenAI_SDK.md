7️⃣ Task 07

https://github.com/panaversity/learn-agentic-ai/tree/main/01_ai_agents_first
https://openai.github.io/openai-agents-python/ref/run/
https://openai.github.io/openai-agents-python/ref/agent/

The Agent class has been defined as a dataclass why?

The system prompt is contained in the Agent class as instructions? Why you can also set it as callable?

But the user prompt is passed as parameter in the run method of Runner and the method is a classmethod

What is the purpose of the Runner class?

What are generics in Python? Why we use it for TContext?


---

The Agent class is defined as a dataclass to simplify the creation of classes that are primarily used to store data.

By using the @dataclass decorator, Python automatically generates special methods like __init__(), __repr__(), and __eq__().

In the context of the OpenAI Agents SDK, the Agent class encapsulates configuration details such as instructions (system prompt), model settings, tools, and other parameters. Defining it as a dataclass ensures that these configurations are organized, readable, and easy to manage. This approach reduces boilerplate code and enhances maintainability.

---

The instructions attribute in the Agent class serves as the system prompt, guiding the behavior of the agent. It can be defined either as a static string or as a callable (function).

 **Static String**: When instructions is a string, it provides a fixed prompt that remains constant across different runs.

**Callable**: Defining instructions as a callable allows for dynamic generation of prompts based on the current context or state. This flexibility is useful when the prompt needs to adapt to varying conditions or inputs.

---

The run method of the Runner class is responsible for executing the agent's logic based on a given user prompt. It is defined as a classmethod to allow invocation without instantiating the Runner class.

By passing the user prompt as a parameter to the run method, the SDK separates the static configuration of the agent (defined in the Agent class) from the dynamic input provided by the user. This separation ensures that the agent's behavior can be consistently managed while still allowing for varied user interactions.

---

The Runner class in the OpenAI Agents SDK orchestrates the execution of agents. It provides methods to run agents in different modes:

**run()**: Executes the agent asynchronously and returns a RunResult.

**run_sync()**: Runs the agent synchronously, suitable for simpler applications.

**run_streamed()**: Allows streaming of the agent's responses, providing real-time feedback.

The Runner handles the agent's decision-making loop, including tool selection and execution, until the task is completed.

---

Generics in Python, introduced through the typing module, allow for the creation of classes and functions that can operate on different data types while maintaining type safety. They are defined using TypeVar and Generic.

In the OpenAI Agents SDK, TContext is a type variable representing the context type that an agent operates on. By using generics for TContext, the SDK allows developers to specify the exact type of context their agent requires, enhancing code clarity and reducing errors.
