# 🎯 Prompt Engineering MCQ - Level 2

### 1. 🌡️ Explain how temperature settings affect LLM outputs. When would you use 0.1 versus 0.9?
A) ✨ Temperature 0.1 produces creative outputs for brainstorming; 0.9 produces focused outputs for factual tasks  
B) 🎯 Temperature 0.1 produces focused, deterministic responses for factual questions; 0.9 produces creative, diverse outputs for poetry  
C) 📏 Temperature 0.1 is for long responses; 0.9 is for short responses  
D) 🔋 Temperature 0.1 uses more computational resources; 0.9 is more efficient

### 2. 🔑 What are the three key temperature settings and when would you use each?
A) ✍️ Low (0-0.3) for creative writing, Medium (0.4-0.7) for math problems, High (0.8-1.0) for factual questions  
B) 🧊 Low (0-0.3) for focused/deterministic responses, Medium (0.4-0.7) for balanced creativity, High (0.8-1.0) for creative/experimental content  
C) 💬 Low (0-0.3) for short answers, Medium (0.4-0.7) for medium answers, High (0.8-1.0) for long answers  
D) ✅ Low (0-0.3) for simple tasks, Medium (0.4-0.7) for moderate tasks, High (0.8-1.0) for complex tasks

### 3. 🧩 What are the six components of the prompting framework, and why is each important?
A) 🤖 Model, Data, Training, Testing, Deployment, Monitoring  
B) 🛠️ Command, Context, Logic, Roleplay, Formatting, Questions  
C) ➡️ Input, Processing, Output, Validation, Storage, Retrieval  
D) 📈 Planning, Execution, Verification, Iteration, Documentation, Optimization

### 4. ⚖️ Describe zero-shot versus few-shot prompting. Give a scenario where each is most appropriate.
A) 🚫 Zero-shot provides examples; few-shot doesn't provide examples. Zero-shot for complex tasks, few-shot for simple tasks  
B) 🎯 Zero-shot asks directly without examples for simple well-defined tasks; few-shot provides multiple examples to establish patterns for tasks needing format guidance  
C) 🔄 Zero-shot uses one model; few-shot uses multiple models. Zero-shot for speed, few-shot for accuracy  
D) 👶 Zero-shot is for beginners; few-shot is for experts. Zero-shot for learning, few-shot for production

### 5. 🧑‍💻 Walk me through how you would structure a prompt for a customer service AI agent. What specific elements must you include and why?
A) 🤷 Just provide the customer query and let the AI figure out the rest  
B) 📝 Include role definition, task breakdown with scenarios (billing, refunds, login issues), escalation protocols, output format, guardrails for tone, and tool access instructions  
C) 📚 Only include the company's FAQ document and basic greeting instructions  
D) 📂 Provide customer history and product catalog without any behavioral guidelines

### 6. 🧠 Explain Chain of Thought prompting. How does it improve reasoning, and what types of problems benefit most from it?
A) 📊 It provides multiple examples to show the pattern; benefits classification tasks  
B) 🪜 It encourages step-by-step reasoning for complex problems; benefits math problems, logical reasoning, and multi-step processes  
C) 🎭 It assigns a role to the AI; benefits creative writing tasks  
D) 📤 It structures the output format; benefits data extraction tasks

### 7. ❓ What is the "Questions" technique in the 6-part framework, and why is it called the "secret sauce"?
A) 🗣️ It asks the user to provide more examples for better training  
B) ✨ It has the AI ask clarifying questions to identify gaps in the prompt and provide more personalized results  
C) 🤔 It questions the AI's responses to verify accuracy  
D) 💬 It creates a question-answer format for the output

### 8. 🤖 Name the six essential components of any AI agent. Why is each necessary?
A) 🌐 Frontend, Backend, Database, API, Authentication, Deployment  
B) 🧠 Model (AI engine), Tools (external system integration), Knowledge/Memory (information storage), Audio/Speech (natural interaction), Guardrails (safety mechanisms), Orchestration (deployment/monitoring)  
C) ➡️ Input, Processing, Output, Storage, Retrieval, Display  
D) 💡 Planning, Reasoning, Acting, Learning, Adapting, Optimizing

### 9. 🧑‍🤝‍🧑 How does Mixture-of-Experts architecture change your approach to prompt engineering? Give three specific strategies.
A) 💬 Use longer prompts, avoid examples, increase temperature  
B) 🎯 Front-load domain signals, use unambiguous domain-specific vocabulary, separate mixed tasks into sequential prompts  
C) 🎨 Use generic language, combine multiple tasks, add creative phrasing  
D) 🚫 Reduce context, use euphemisms, mix formats freely

### 10. ↔️ Compare Step-Back Prompting with Self-Consistency. When would you choose one over the other?
A) 🛣️ Step-Back asks a general question first then uses that context for specific questions; Self-Consistency generates multiple reasoning paths and selects the most common answer  
B) 🎨 Step-Back is for creative tasks; Self-Consistency is for factual tasks  
C) 🤖 Step-Back uses one model; Self-Consistency uses multiple models  
D) ⚡ Step-Back is faster; Self-Consistency is more accurate in all cases

### 11. 📚 You're building a research assistant that needs to handle multiple source types. Design the context engineering strategy, including how you'd structure the system prompt.
A) 🙈 Just provide access to all sources without any structure or instructions  
B) 🏗️ Define role, break down tasks by source type (news, X, Reddit, academic), specify prioritization criteria (engagement, authority), define JSON output format, set time constraints, include summarization requirements  
C) 🔬 Only focus on one source type and ignore the others  
D) 🧠 Let the AI decide which sources to use without guidance

### 12. ⚙️ Explain the four advanced context engineering strategies: writing, selecting, compressing, and isolating context. Give a use case for each.
A) 📝 Writing (task notes), Selecting (database queries for relevant data), Compressing (summarization techniques), Isolating (task-specific context separation)  
B) 💻 Writing (code generation), Selecting (model selection), Compressing (token reduction), Isolating (error handling)  
C) 📄 Writing (documentation), Selecting (user preferences), Compressing (data encryption), Isolating (security protocols)  
D) 📜 Writing (logs), Selecting (features), Compressing (optimization), Isolating (testing)

### 13. 🛠️ An MoE model gives inconsistent answers across runs for the same prompt. Diagnose the problem and propose three solutions.
A) ❌ The model is broken; switch to a different model, increase memory, reduce complexity  
B) 🚦 Routing instability causing different expert activation; solutions: add sharper domain anchors at the top, reduce temperature, include one short in-domain example  
C) 🌐 Network latency issues; solutions: use faster internet, cache responses, reduce prompt length  
D) 🚫 Token limit exceeded; solutions: shorten prompt, remove examples, simplify language

### 14. 📝 Critique this prompt: "Write about dogs." What's wrong, and how would you fix it using the 6-part framework?
A) 👍 Nothing wrong; it's clear and concise  
B) ✏️ Too vague - lacks command specificity, context, logic/structure, roleplay, formatting, and questions. Fix: "Create a 300-word informative article about health benefits of owning dogs, focusing on mental health and physical activity, using friendly tone for general readers, formatted with headers and bullet points"  
C) ➡️ Too short; just make it longer without changing structure  
D) 🐶 Wrong topic; change to cats instead

### 15. ⬆️ Why does the material emphasize "front-loading domain signals" for MoE models? Explain the routing mechanism and its implications.
A) 💰 To save tokens and reduce costs  
B) 🧭 Because the router chooses experts based on tokens, and early domain signals help lock onto the right experts early, improving response quality  
C) 👔 To make prompts look more professional  
D) 📜 To comply with model requirements

### 16. 🏦 Design a complete prompt for a financial analysis agent that demonstrates all six framework components plus context engineering principles.
A) 📉 "Analyze this financial data"  
B) 📈 Command: "Recommend comprehensive investment strategy"; Context: specific user details (age, income, goals); Logic: define output structure; Roleplay: certified financial advisor role; Formatting: executive summary, tables, milestones; Questions: "Ask 10 questions to tailor strategy"  
C) 📊 Just provide the financial data without any instructions  
D) 📄 Use a generic template without customization

### 17. 🗣️ Give an example of a weak command verb and a strong command verb.
A) 👎 Weak: "Analyze"; Strong: "Give"  
B) 💪 Weak: "Give" or "Help"; Strong: "Analyze", "Create", "Recommend", "Evaluate"  
C) 🤷 Weak: "Create"; Strong: "Maybe"  
D) 🚫 Weak: "Recommend"; Strong: "Try"

### 18. ➕ Explain the "Rule of Three" for providing context.
A) 📝 Use exactly three sentences in every prompt  
B) 🧑‍🤝‍🧑 Provide context across three dimensions: Who (age, profession, situation), What (specific goal, constraints), When (timeline, deadlines)  
C) ❓ Ask three questions before providing an answer  
D) 🤖 Use three different models for comparison

### 19. 📸 How do you maintain consistency with a reference photo in Nano Banana?
A) 🖼️ This question relates to image generation prompting, which is covered in a separate tutorial not included in the provided context  
B) 🌡️ Use the same temperature setting for all generations  
C) 📋 Copy the exact same prompt every time  
D) 🔄 Use the same model version consistently

### 20. ☀️ What is "golden hour" lighting and why is it flattering for portraits?
A) 🖼️ This question relates to image generation prompting techniques, which is covered in a separate tutorial not included in the provided context  
B) 🌑 Lighting at noon that creates harsh shadows  
C) 💡 Artificial studio lighting setup  
D) 🌃 Low-light photography technique