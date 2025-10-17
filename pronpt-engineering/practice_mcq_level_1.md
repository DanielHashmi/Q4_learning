# 🎯 Prompt Engineering MCQ - Level 1

## 📚 Question 1: Fundamental Distinction
**Which statement most accurately distinguishes prompt engineering from context engineering in LLM applications?**

- A) Prompt engineering focuses on model selection while context engineering focuses on temperature settings
- B) ✅ Prompt engineering crafts instructions on how the model should behave, while context engineering curates the information the model can access `readme.md:84-86`
- C) Prompt engineering is for chatbots while context engineering is for agents
- D) Prompt engineering uses JSON schemas while context engineering uses XML tags

**Answer: B**

---

## ⚙️ Question 2: Configuration Parameters
**In a scenario requiring deterministic, factual responses for mathematical computations, which configuration would be most appropriate?**

- A) Temperature 0.9, Top-P 0.99, Top-K 40
- B) Temperature 0.7, Top-P 0.95, Top-K 30
- C) ✅ Temperature 0.1, Top-P 0.9, Top-K 20 `readme.md:148-154`
- D) Temperature 0.5, Top-P 0.85, Top-K 25

**Answer: C**

---

## 🧠 Question 3: Advanced Prompting Strategy
**The ReAct (Reasoning + Acting) prompting pattern is characterized by:**

- A) Generating multiple reasoning paths and selecting the most common answer
- B) Asking general questions before specific ones to establish context
- C) ✅ Interleaving reasoning steps (Thoughts) with actions (tool calls) in an iterative loop until goal resolution `readme.md:400-401`
- D) Exploring multiple reasoning branches simultaneously for complex problems

**Answer: C**

---

## 🔧 Question 4: Context Engineering Implementation
**In a RAG-based policy Q&A system, which approach best demonstrates proper separation of prompt and context engineering concerns?**

- A) Embedding all policy documents directly in the system prompt with extraction instructions
- B) ✅ Using prompt engineering to define answer format and citations, while context engineering handles chunking, metadata filtering, and retrieval ranking `readme.md:110-113`
- C) Relying solely on few-shot examples to teach the model about policies
- D) Setting high temperature values to encourage creative policy interpretations

**Answer: B**

---

## 🎭 Question 5: Mixture-of-Experts (MoE) Architecture
**How does the MoE architecture fundamentally change prompt engineering practices compared to dense models?**

- A) MoE models require longer prompts with more examples
- B) MoE models eliminate the need for structured prompts entirely
- C) ✅ Front-loading domain-specific signals becomes critical because the gating network routes tokens to specialized experts based on early input patterns `readme.md:826-832`
- D) MoE models only work with zero-shot prompting techniques

**Answer: C**

---

## 🔗 Question 6: Chain of Thought (CoT) Application
**When implementing Chain of Thought prompting for complex reasoning tasks, which practice is most critical for consistent results?**

- A) Using high temperature settings (0.8-1.0) to encourage diverse reasoning paths
- B) ✅ Setting temperature to 0 for consistent reasoning and extracting final answers separately from reasoning steps `readme.md:290-293`
- C) Avoiding step-by-step phrases to let the model reason naturally
- D) Combining multiple reasoning strategies in a single prompt

**Answer: B**

---

## ⚠️ Question 7: Context Engineering Failure Modes
**Which scenario best illustrates a context engineering failure rather than a prompt engineering failure?**

- A) The model returns unstructured text instead of the requested JSON format
- B) ✅ The model hallucinates outdated information because relevant documents weren't retrieved from the knowledge base `readme.md:89-94`
- C) The model misunderstands vague instructions about output length
- D) The model uses an inappropriate tone for the target audience

**Answer: B**

---

## 🎲 Question 8: Self-Consistency Strategy
**The Self-Consistency prompting technique improves reliability by:**

- A) Using the same prompt repeatedly with identical parameters until convergence
- B) ✅ Generating multiple reasoning paths with varied approaches and selecting the most frequently occurring result `readme.md:296-320`
- C) Asking the model to verify its own answer through self-critique
- D) Combining outputs from different LLM models

**Answer: B**

---

## 🚀 Question 9: MoE Routing Optimization
**In MoE models, which prompt structure element has the LEAST impact on expert routing efficiency?**

- A) Domain-specific vocabulary in the opening lines
- B) Clear task type specification (e.g., "quantitative proof/derivation")
- C) ✅ The total character count of the prompt
- D) Language specification for multilingual models `readme.md:830-841`

**Answer: C**

---

## 🌳 Question 10: Tree of Thoughts (ToT) Methodology
**Tree of Thoughts differs from standard Chain of Thought by:**

- A) Using simpler, linear reasoning paths
- B) ✅ Exploring multiple reasoning branches simultaneously, evaluating each, and synthesizing the best ideas `readme.md:446-447`
- C) Eliminating the need for step-by-step reasoning
- D) Focusing exclusively on creative tasks rather than analytical ones

**Answer: B**
