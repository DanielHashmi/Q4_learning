# 100 Easy MCQs: General Agents Foundations (Across 12, 13, 14)

> Covering Chapters 12, 13, and 14 — The AI Agent Factory Paradigm, Markdown, and Working with General Agents (Claude Code & Cowork)

---

## Chapter 12 — The AI Agent Factory Paradigm

---

**Q1.** At the September 2025 ICPC World Finals in Baku, Azerbaijan, what was remarkable about Problem C?

- A) It was solved only by the winning human team from St. Petersburg State University
- B) It was solved by both OpenAI and Gemini but by none of the 139 human teams
- C) It was unsolvable by AI within the 5-hour time limit
- D) It was solved exclusively by Google DeepMind's Gemini 2.5 Deep Think

**Answer: B**

---

**Q2.** According to the GDPval Benchmark (September 2025), what was Claude Opus 4.1's win rate against human expert programmers?

- A) 15%
- B) 40.6%
- C) 49%
- D) 76%

**Answer: C**

---

**Q3.** The DORA 2025 Report found that developers spent a median of how many hours per day collaborating with AI?

- A) 30 minutes
- B) 1 hour
- C) 2 hours
- D) 4 hours

**Answer: C**

---

**Q4.** Which company announced a $1.1 billion acquisition of Sana — a company building AI-powered workplace agents — in September 2025?

- A) Microsoft
- B) Salesforce
- C) Workday
- D) ServiceNow

**Answer: C**

---

**Q5.** The content describes the global developer economy as approximately $3 trillion. Which two figures are multiplied to reach this estimate?

- A) 10 million developers × $300,000/year
- B) 30 million developers × $100,000/year
- C) 50 million developers × $60,000/year
- D) 20 million developers × $150,000/year

**Answer: B**

---

**Q6.** Why is software's self-disruption considered "faster and more complete" than disruption experienced by agriculture or manufacturing?

- A) Software companies have larger budgets for R&D
- B) When software disrupts itself, tools, workflows, and mental models all shift simultaneously with no gradual adaptation option
- C) Software developers have higher educational attainment than farmers or factory workers
- D) Software is distributed digitally, allowing faster rollout

**Answer: B**

---

**Q7.** In the Agent Maturity Model, what is the defining characteristic of Stage 1 (The Incubator)?

- A) Executing pre-defined workflows with maximum reliability
- B) Enforcing hard governance constraints on AI behavior
- C) Transforming raw, ambiguous requirements into functional solutions through exploration and iteration
- D) Scaling a known solution to thousands of production requests

**Answer: C**

---

**Q8.** According to the content, what is the role of a human when working with a General Agent (Incubator)?

- A) Auditor
- B) Director
- C) Builder
- D) Governor

**Answer: B**

---

**Q9.** Which of the following is NOT one of the four responsibilities of a "Director" when working with a General Agent?

- A) Set the Intent
- B) Provide Access (the "dossier")
- C) Build Guardrails
- D) Course Correct

**Answer: C**

---

**Q10.** What does the content mean by "dynamic planning" in the context of agentic development?

- A) The human creates a detailed plan and the agent follows it step by step
- B) The agent plans from scratch without pre-defined templates, decomposing goals on the fly
- C) Plans are updated dynamically based on real-time market data
- D) Multiple agents race to produce plans and the fastest one wins

**Answer: B**

---

**Q11.** Which General Agent tool is described as originating from Block (now Square) and being hosted by the Agentic AI Foundation, excelling at tasks requiring visual understanding and web-based execution?

- A) Claude Code
- B) OpenAI Codex CLI
- C) Gemini CLI
- D) Goose

**Answer: D**

---

**Q12.** What does the content call the "genetic material" produced by successful incubation?

- A) A compiled binary ready for deployment
- B) Crystallized understanding — working solutions, discovered requirements, patterns, edge cases, and proven architecture
- C) A Custom Agent SDK with pre-built guardrails
- D) An AGENTS.md file ready for version control

**Answer: B**

---

**Q13.** Which Custom Agent SDK is described as having "deep integration with Claude's reasoning capabilities, multi-turn conversation continuity and state management"?

- A) OpenAI Agents SDK
- B) Google ADK
- C) Claude Agent SDK
- D) Gemini Agent Kit

**Answer: C**

---

**Q14.** In the comparison table between General Agents and Custom Agents, which characteristic correctly describes Custom Agents?

- A) Variable reliability (creative means unpredictable)
- B) Higher per-request cost (exploration is expensive)
- C) Harder governance (flexibility resists constraints)
- D) Consistent reliability (same inputs → same outputs)

**Answer: D**

---

**Q15.** Which of the following is identified as an anti-pattern called "Perpetual Incubation"?

- A) Building a Custom Agent before requirements stabilize
- B) Using General Agents for high-volume production workloads
- C) Skipping incubation and specifying a Custom Agent without exploration
- D) Retiring the General Agent after deploying the Specialist

**Answer: B**

---

**Q16.** What is the key insight of the "Agent Factory" paradigm regarding the relationship between General Agents and Custom Agents?

- A) General Agents compete with Custom Agents for the same tasks
- B) Custom Agents are always superior and replace General Agents
- C) General Agents don't compete with Custom Agents — General Agents BUILD Custom Agents
- D) Custom Agents build General Agents iteratively

**Answer: C**

---

**Q17.** According to the Three Core Operational Constraints of LLMs, what is the correct explanation for why a chatbot session appears to "remember" earlier messages?

- A) The LLM stores session data in a persistent memory layer between API calls
- B) The application re-sends the entire conversation history with every new message; the model reads it fresh each time
- C) The LLM's weights are fine-tuned during the session to retain context
- D) A separate retrieval-augmented generation (RAG) module injects memories

**Answer: B**

---

**Q18.** What is the purpose of a file like AGENTS.md or SPEC.md in the context of LLM statelessness?

- A) To serve as executable code that the agent runs at startup
- B) To provide persistent context that gets re-injected into every session, countering statelessness
- C) To lock the LLM's temperature to zero for deterministic output
- D) To define the deployment environment and cloud provider

**Answer: B**

---

**Q19.** The content states that LLMs are "probabilistic, not deterministic." What does a temperature setting of 0 mean for a frontier model?

- A) The model always generates the most creative response
- B) The model refuses to generate code
- C) The model always picks the highest-probability token (more deterministic, less creative)
- D) The model's output is guaranteed to be identical every run without exception

**Answer: C**

---

**Q20.** Which of the following best explains the "lost in the middle" effect related to context windows?

- A) Files in the middle of a codebase are harder for the model to locate
- B) Information placed in the center of a very long context receives less attention than content at the beginning or end
- C) Tokens in the middle of a sentence are processed with lower accuracy
- D) The agent loses track of its place in a multi-step task

**Answer: B**

---

**Q21.** As of early 2026, which frontier model has the largest context window according to the content?

- A) Claude Opus 4.5 (200K tokens)
- B) GPT-5.2 (256K tokens)
- C) Gemini 3 Pro (2M tokens)
- D) Claude Sonnet 4.6 (500K tokens)

**Answer: C**

---

**Q22.** According to the content, how does Spec-Driven Development (SDD) address all three LLM constraints simultaneously?

- A) It uses external databases to eliminate statelessness, temperature clamping, and infinite context caching
- B) Specifications persist across sessions (counters statelessness), constrain probabilistic outputs (reduces variation), and compress intent efficiently (respects context limits)
- C) It replaces LLMs with deterministic rule-based systems for production
- D) It mandates that developers write all code manually before showing it to the AI

**Answer: B**

---

**Q23.** Satya Nadella's "Full-Stack Builder" concept, mentioned in relation to the Orchestrator role, describes what transformation?

- A) Developers who specialize even more deeply in one language or framework
- B) Developers who merge the roles of product manager, designer, frontend engineer, and backend engineer because AI handles implementation details across all layers
- C) Teams that outsource all development to offshore contractors
- D) Managers who build their own apps without any AI assistance

**Answer: B**

---

**Q24.** In the Five Generations of AI Tools, what primarily defines Generation 4 (Agentic Mainstream) as of 2024–2026?

- A) AI that only autocompletes single lines of code
- B) AI that generates entire functions from chat prompts alone
- C) AI tools using MCP to connect to databases/logs/Jira, handling multi-step orchestration, with the human role shifting to Orchestrator
- D) Fully self-evolving AI that monitors production without human involvement

**Answer: C**

---

**Q25.** What is the human role described for Generation 5 (Self-Evolving Ecosystems / Resident AI)?

- A) Typist
- B) Prompt Engineer
- C) Orchestrator
- D) Policy Governor

**Answer: D**

---

**Q26.** The content describes SaaS as solving the "deployment problem." What problem do AI agents solve, according to the content?

- A) The pricing problem (making software cheaper)
- B) The intelligence problem (agents don't just help humans do cognitive work, they do the work)
- C) The design problem (making interfaces more intuitive)
- D) The security problem (eliminating vulnerabilities automatically)

**Answer: B**

---

**Q27.** Which of the following correctly describes what a Digital FTE (Full-Time Equivalent) does, according to the content?

- A) It augments human tasks by providing suggestions and autocomplete
- B) It performs real work autonomously end-to-end (processing support tickets, analyzing documents, generating reports) under human supervision
- C) It replaces the need for any human oversight in enterprise workflows
- D) It acts as a chatbot that answers employee questions

**Answer: B**

---

**Q28.** The content states that Digital FTEs work 168 hours per week. What does this figure represent?

- A) The maximum hours a Digital FTE can be billed per month
- B) 24 hours × 7 days — a full week of continuous autonomous operation
- C) The number of tasks processed per week at peak load
- D) The combined hours of three human employees working full time

**Answer: B**

---

**Q29.** The OODA Loop (Observe, Orient, Decide, Act) is used to explain how agentic AI reasons. What is the key difference between how a passive AI (like ChatGPT without tools) and an agentic AI use this loop?

- A) Passive AI uses OODA; agentic AI uses a simpler two-step process
- B) Passive AI predicts (responds once); agentic AI cycles through OODA repeatedly until the goal is achieved
- C) OODA is exclusive to military strategy and doesn't apply to AI agents
- D) Agentic AI uses OODA only for planning, not for execution

**Answer: B**

---

**Q30.** The "Five Powers" of AI agents are See, Hear, Reason, Act, and Remember. In the hotel-booking example, which power enables the agent to recall the user's preference for quiet rooms without being told again?

- A) See
- B) Hear
- C) Act
- D) Remember

**Answer: D**

---

**Q31.** In the Modern AI Stack (2026), what does MCP stand for and what is its role?

- A) Machine Communication Protocol — manages API rate limits
- B) Model Context Protocol — serves as the "USB cable" connecting agents to databases, Slack, Jira, and other external systems
- C) Modular Coding Pipeline — orchestrates multi-step code generation
- D) Memory Context Processor — handles long-term storage for LLMs

**Answer: B**

---

**Q32.** According to the 2026 Modern AI Stack, what is the role of "Agent Skills" compared to MCP?

- A) MCP is the "App" that teaches the agent how to use a connection; Skills are the "USB Cable" providing connectivity
- B) MCP is the "USB Cable" (connects agents to tools); Agent Skills are the "App" (teaches agents how to use those connections to achieve goals)
- C) Agent Skills replace MCP entirely in the 2026 stack
- D) Both MCP and Agent Skills are deprecated in favor of direct API calls

**Answer: B**

---

**Q33.** What is "Bidirectional Sampling" introduced in the late 2025 MCP update?

- A) A technique for the LLM to sample from two different models simultaneously
- B) An MCP Server (like a database) can ask the LLM a question mid-execution, enabling richer two-way interaction
- C) A method for parallel agent teams to share context
- D) A security mechanism preventing unauthorized MCP connections

**Answer: B**

---

**Q34.** What is the AIFF (Agentic AI Foundation)? When was it formed and which organizations donated founding projects?

- A) Formed in January 2026; Anthropic, Google, and Microsoft donated all three founding projects
- B) Formed on December 9, 2025; OpenAI donated AGENTS.md, Anthropic donated MCP, and Block donated Goose, all to the Linux Foundation
- C) Formed in 2024; GitHub donated Copilot, OpenAI donated GPT-4, and Google donated Gemini
- D) Formed in March 2026; it is a private industry consortium with paid membership

**Answer: B**

---

**Q35.** The Nine Pillars of AIDD (AI-Driven Development) is referenced in Chapter 12. Which of the following is listed as a required skill for AI-native development that traditional CS education does NOT typically teach?

- A) Algorithm optimization and manual debugging
- B) Syntax mastery in low-level languages
- C) Specification writing (clear specs determine AI output quality)
- D) Understanding of CPU architecture

**Answer: C**

---

**Q36.** What does "Progressive Disclosure" mean in the context of the Agent Skills Standard (agentskills.io)?

- A) Skills gradually reveal their pricing over time
- B) An agent reads the full SKILL.md upfront before starting any task
- C) An agent reads Skill Metadata (name, description) first and only loads full instructions when the task specifically requires them
- D) Skills are disclosed to competitors only after a progressive delay

**Answer: C**

---

**Q37.** The content describes "Skill Portability." What does this mean practically?

- A) Skills can be exported to other countries for use in different legal jurisdictions
- B) A Skill written for Claude Code also works in Gemini CLI or OpenAI Codex without modification
- C) Skills can be transferred between different employees in an organization
- D) Skills can be converted from SKILL.md format to executable binary

**Answer: B**

---

**Q38.** In the AI-Driven Development (AIDD) three-layer model, what is the developer's responsibility in Layer 1 (Intent Layer)?

- A) Write production code that will be deployed to servers
- B) Train the LLM on domain-specific data
- C) Define what should be built and have final approval authority over the specification
- D) Configure API keys and cloud infrastructure

**Answer: C**

---

**Q39.** What is described as the key signal for "Premature Specialization" (an anti-pattern)?

- A) Using General Agents for tasks that run only once
- B) Building a Custom Agent before requirements have crystallized, resulting in over-engineered solutions to the wrong problem
- C) Deploying a Custom Agent without monitoring or logging
- D) Hiring too many human engineers alongside an AI system

**Answer: B**

---

**Q40.** According to the SDLC transformation described in Chapter 12, how does AI change the "Coding" phase specifically?

- A) AI eliminates the coding phase entirely; only planning and testing remain
- B) The developer's role shifts from typing implementations (4–8 hours) to specifying clearly and validating AI output (30 minutes)
- C) AI writes comments and documentation while humans write all code
- D) AI takes over deployment but leaves coding entirely to humans

**Answer: B**

---

## Chapter 13 — Markdown Writing Instructions

---

**Q41.** According to Chapter 13, what is the primary reason structured markdown results in dramatically better AI-generated code compared to unstructured plain text?

- A) Markdown files are processed faster by LLMs due to smaller file sizes
- B) Markdown removes ambiguity by giving each requirement a distinct label, allowing the AI to parse exactly how many features exist and in what order
- C) AI models are exclusively trained on markdown files from GitHub
- D) Markdown automatically generates unit tests for the described features

**Answer: B**

---

**Q42.** In the AIDD three-layer model from Chapter 13, what is markdown's specific role?

- A) It functions as Layer 3 (Implementation Layer) where code is generated
- B) It is the bridge in Layer 1 (Intent Layer), expressing human intent in structured form that bridges what you want and what AI builds
- C) It is an optional enhancement applied only in Layer 2 (Reasoning Layer)
- D) Markdown replaces all three layers in simpler projects

**Answer: B**

---

**Q43.** Markdown was created in 2004 by John Gruber. What is the name of the formal specification standard for markdown that began in 2014?

- A) GitHub Flavored Markdown (GFM)
- B) StandardMark
- C) CommonMark
- D) OpenMark

**Answer: C**

---

**Q44.** GitHub Flavored Markdown (GFM) extends CommonMark with three specific features. Which combination is correct?

- A) Tables, footnotes, and embedded videos
- B) Tables, task lists (`- [ ]`), and strikethrough (`~~text~~`)
- C) Code highlighting, diagrams, and LaTeX math
- D) Task lists, color themes, and custom fonts

**Answer: B**

---

**Q45.** At the technical level (tokens and attention), why does structured markdown improve LLM comprehension compared to continuous prose?

- A) Markdown compresses tokens using a special encoding scheme
- B) Headings like `## Features` create attention cues that focus the model's attention mechanism on relevant sections instead of treating the document as one continuous stream
- C) Markdown prevents the model from hallucinating by limiting vocabulary
- D) Structured text reduces the context window usage by 50%

**Answer: B**

---

**Q46.** Which markdown heading level should be used exactly ONCE in a specification document and only at the very top?

- A) `##` (Level 2)
- B) `###` (Level 3)
- C) `#` (Level 1)
- D) `####` (Level 4)

**Answer: C**

---

**Q47.** What is wrong with the following markdown heading structure?

```
# My App
### Installation Steps
## User Guide
```

- A) Level 2 (`##`) should never appear in a specification document
- B) Level 3 (`###`) skips Level 2 — the hierarchy is broken because you cannot go from Level 1 directly to Level 3 without an intermediate Level 2
- C) The `# My App` title should use Level 2 (`##`) instead
- D) There is nothing wrong with this structure

**Answer: B**

---

**Q48.** According to Chapter 13, what is the correct syntax to create a Level 2 heading in markdown?

- A) `* Heading`
- B) `-- Heading`
- C) `## Heading`
- D) `<h2>Heading</h2>`

**Answer: C**

---

**Q49.** Why does the content state that proper heading hierarchy matters beyond just visual style?

- A) It affects how GitHub calculates repository statistics
- B) It is essential for accessibility (screen readers navigate by heading levels) and machine parsing (AI agents use hierarchy to understand document structure and relationships)
- C) Skipping levels causes markdown renderers to throw errors and refuse to display the file
- D) It determines how the specification is indexed in search engines

**Answer: B**

---

**Q50.** In Chapter 13's Verification Framework for AI responses, what should you do BEFORE accepting an AI's claim that your markdown is correct?

- A) Post the markdown to a public forum and wait for community feedback
- B) Ask the AI to implement the specification; if the generated code doesn't match what you wanted, your spec wasn't actually clear
- C) Immediately submit the specification to GitHub without further review
- D) Convert the markdown to PDF and check the rendering

**Answer: B**

---

**Q51.** A developer writes a markdown specification with an unstructured paragraph describing a weather app. The AI generates a two-line script that's missing humidity, wind speed, and error handling. The developer rewrites it with a structured `## Features` list and a numbered `## User Flow`. What explains the dramatic improvement in the second AI output?

- A) The second prompt used a longer context window
- B) The AI model was updated between the two requests
- C) The structured version gave the AI distinct, countable items (each feature as a separate bullet) and a clear sequence (numbered steps), eliminating ambiguity about what to build
- D) Markdown files are automatically run through a more powerful AI model

**Answer: C**

---

**Q52.** Chapter 13 lists four real-world contexts where markdown is used. Which of the following is NOT listed as a real-world markdown use case in the content?

- A) GitHub README files for project documentation
- B) Specifications for AI agents that build software
- C) Replacing SQL database schemas in backend systems
- D) AI chat prompts structured to get better code generation results

**Answer: C**

---

**Q53.** When should Level 5 (`#####`) and Level 6 (`######`) headings be avoided in specifications, according to Chapter 13?

- A) When the specification is shorter than 500 words
- B) In all cases — headings only go up to Level 4
- C) When they would be needed at all in a specification, because needing them signals the document structure is too complex
- D) Whenever the document will be rendered on GitHub

**Answer: C**

---

**Q54.** According to the Task Tracker App exercise in Chapter 13, which heading structure correctly places Level 3 subsections under the Features section?

- A) `# Task Tracker App → ## Add Tasks → ### Features`
- B) `# Task Tracker App → ## Features → ### Add Tasks`
- C) `## Task Tracker App → # Features → ### Add Tasks`
- D) `# Task Tracker App → ### Features → ## Add Tasks`

**Answer: B**

---

**Q55.** What is a common mistake in markdown heading syntax that prevents proper rendering?

- A) Using too many words in a heading
- B) Writing `#Heading Without Space` — forgetting the mandatory space after the hash symbol
- C) Placing a heading at the start of a document
- D) Mixing uppercase and lowercase in heading text

**Answer: B**

---

## Chapter 14 — Working with General Agents: Claude Code and Cowork

---

**Q56.** Who discovered the "Product Overhang" concept that led to Claude Code, and what did he do in September 2024 that unlocked it?

- A) Dario Amodei ran a competition to see which Anthropic model could pass coding interviews
- B) Boris Cherny joined Anthropic and gave Claude direct access to the filesystem, revealing that the capability to explore codebases already existed but needed the right product interface
- C) An external contractor discovered that Claude could write its own documentation autonomously
- D) The Claude Code team at Anthropic reverse-engineered GitHub Copilot's architecture

**Answer: B**

---

**Q57.** What happened on Day 1 of Claude Code's internal (dogfooding) release at Anthropic in November 2024?

- A) The team shut it down due to too many errors
- B) 20% of Anthropic engineers adopted it on the first day
- C) It was used exclusively by the Claude Code engineering team, not broader Anthropic
- D) 80% of engineers adopted it immediately on day one

**Answer: B**

---

**Q58.** By November 2025, what annual run-rate revenue had Claude Code generated, and what was the primary growth mechanism?

- A) $100M ARR, driven primarily by paid advertising
- B) $500M ARR, driven mainly by word-of-mouth
- C) $1B ARR, driven almost entirely by word-of-mouth
- D) $2.5B ARR, driven by enterprise sales teams

**Answer: C**

---

**Q59.** The content states that approximately what percentage of Claude Code was written by Claude Code itself?

- A) 25%
- B) 50%
- C) 75%
- D) 90%

**Answer: D**

---

**Q60.** What is the fundamental difference between "passive AI" (like ChatGPT without file access) and "agentic AI" (like Claude Code), according to Chapter 14?

- A) Passive AI uses a larger model; agentic AI uses a smaller but faster model
- B) Passive AI predicts responses and cannot verify suggestions; agentic AI sees your actual code, runs tests, sees errors, and iterates until the goal is achieved
- C) Passive AI is free; agentic AI requires a subscription
- D) Passive AI operates in the cloud; agentic AI runs entirely on your local machine

**Answer: B**

---

**Q61.** Cowork was launched in January 2026 as a response to what barrier Claude Code encountered?

- A) Claude Code was too expensive for enterprise customers
- B) The terminal was a barrier for non-developers; Cowork brings the same agentic architecture to a familiar Desktop App GUI for knowledge workers
- C) Claude Code could not process documents larger than 10MB
- D) Cowork was launched to replace Claude Code entirely

**Answer: B**

---

**Q62.** What does CLAUDE.md contain, and when is it loaded by Claude Code?

- A) CLAUDE.md is an executable script run when you type `claude --init`; it installs dependencies
- B) CLAUDE.md is a markdown file placed in the project root that Claude Code automatically loads at the start of every session, providing persistent project context
- C) CLAUDE.md stores API keys and authentication tokens for Claude Code
- D) CLAUDE.md is automatically generated by GitHub Actions to document code changes

**Answer: B**

---

**Q63.** What does the `/init` command do in Claude Code?

- A) Initializes a new git repository in the current directory
- B) Resets Claude Code to factory settings and clears all session history
- C) Analyzes the codebase and generates a CLAUDE.md with build commands, test instructions, and project conventions
- D) Creates a new MCP server configuration file

**Answer: C**

---

**Q64.** Why does the content say that "session continuity is an application feature, not a model feature"?

- A) Because Claude Code sessions use a proprietary cloud protocol unavailable to other applications
- B) Because the LLM model itself is stateless — tools like Claude Code maintain continuity by re-injecting the conversation history with every message, not because the model remembers
- C) Because application developers have disabled memory in LLMs for security reasons
- D) Because stateful models would require too much compute to serve at scale

**Answer: B**

---

**Q65.** What is the difference between CLAUDE.md and AGENTS.md, according to the content?

- A) CLAUDE.md is deprecated; AGENTS.md is the only supported standard
- B) CLAUDE.md contains Claude-specific features (skills, hooks, MCP configs); AGENTS.md is a universal cross-vendor standard (adopted by 60,000+ open source projects) for project instructions that work across all AI coding agents
- C) CLAUDE.md is read by Cowork; AGENTS.md is read by Claude Code
- D) There is no difference — they are interchangeable file names

**Answer: B**

---

**Q66.** What is the permission model in Claude Code regarding file writes and terminal command execution?

- A) Claude Code executes all actions immediately without asking for permission
- B) Claude Code requires written approval for every file read as well as every file write
- C) Claude Code shows what it's about to do and waits for your approval before writing files or running commands; reading files does not require approval
- D) Permissions are managed solely through the Claude.ai web dashboard

**Answer: C**

---

**Q67.** An Agent Skill is defined in the content as what?

- A) A set of API endpoints that Claude Code calls to perform actions
- B) Encoded expertise — a SKILL.md document that teaches Claude a precise procedure, reasoning pattern, or domain knowledge; a "plugin for intelligence"
- C) A trained fine-tuned model optimized for a specific task
- D) A configuration file that sets Claude Code's temperature and token limits

**Answer: B**

---

**Q68.** What is "Progressive Disclosure" in the Agent Skills Standard at the tool level?

- A) Skills reveal their pricing tiers progressively over time
- B) Skills are disclosed to enterprise customers before public release
- C) An agent reads the Skill Metadata (name and description) first and only loads the full instructions and scripts when the task specifically requires those Skills
- D) Instructions in a Skill gradually increase in complexity as the agent gains experience

**Answer: C**

---

**Q69.** In Claude Code, what is a "Subagent" and what is the primary reason to use one?

- A) A subagent is a junior developer who reviews Claude's output before submission
- B) A subagent is a separate Claude Code instance spawned to work on an isolated task in parallel, enabling multi-agent parallelism and allowing the orchestrator to delegate focused subtasks
- C) A subagent is a smaller, cheaper LLM model used for background formatting tasks
- D) A subagent is an automated test runner that validates Claude's code output

**Answer: B**

---

**Q70.** The "Ralph Wiggum Loop" is mentioned in Chapter 14 as an autonomous iteration workflow pattern. Based on the context of autonomous iteration, what is the most likely description of this pattern?

- A) A one-shot task that completes and immediately terminates
- B) An autonomous loop where Claude Code iteratively tries, fails, self-corrects, and retries until a goal is achieved — mimicking persistent autonomous problem-solving
- C) A pattern where the human types the same prompt repeatedly until the AI succeeds
- D) A scheduled batch job that runs once every 24 hours

**Answer: B**

---

**Q71.** What are Claude Code "Hooks," and what event types do they respond to?

- A) Hooks are MCP server plugins that add new tools to Claude
- B) Hooks are event-driven automation scripts that fire on specific Claude Code events (like before/after a tool runs), enabling automated quality gates and safety rules
- C) Hooks are keyboard shortcuts that trigger common Claude Code actions
- D) Hooks are webhooks that send notifications to external services when Claude finishes a task

**Answer: B**

---

**Q72.** In the Settings Hierarchy for Claude Code, what is the order of precedence (most specific overrides least specific)?

- A) Enterprise → Project → Global → Directory
- B) Global → Project → Directory (most specific wins)
- C) User → Global → Project → Task
- D) All settings have equal precedence; the last one loaded wins

**Answer: B**

---

**Q73.** What are Claude Code "Worktrees," according to the Chapter 14 table of contents and content context?

- A) Tree-shaped diagrams of Claude's reasoning process
- B) Git worktrees used to run parallel Claude Code agent sessions in isolated branches, preventing one agent's changes from interfering with another
- C) File system structures that organize Claude's output by project
- D) Visual workflow diagrams generated by Claude Code to plan tasks

**Answer: B**

---

**Q74.** What is the "Claude Code Router" (CCR) used in the Free Claude Code Setup lesson?

- A) A network router that prioritizes Claude Code API traffic
- B) A proxy service (`@musistudio/claude-code-router`) that lets Claude Code's agentic architecture use alternative LLM backends (Gemini, DeepSeek, OpenRouter) instead of Anthropic's models
- C) A load balancer that distributes tasks across multiple Claude instances
- D) A GUI application that replaces the terminal for Claude Code users

**Answer: B**

---

**Q75.** According to the Free Claude Code Setup, what is a key operational requirement for DeepSeek's pricing model compared to Gemini's free tier?

- A) DeepSeek requires a minimum monthly commitment of $100
- B) DeepSeek uses token-based pricing ($0.028–$0.42 per million tokens), not a truly free tier, while Gemini offers daily request limits at no cost
- C) DeepSeek only works on Linux; Gemini works on all platforms
- D) DeepSeek requires enterprise credentials while Gemini is open to anyone

**Answer: B**

---

**Q76.** What is the recommended Windows installation method for Claude Code, and why?

- A) npm install, because it works universally across all Node.js versions
- B) WinGet, because it integrates with Windows Update for automatic patches
- C) WSL (Windows Subsystem for Linux) using `curl -fsSL https://claude.ai/install.sh | bash`, because it provides a full Linux environment with the best compatibility, as recommended by Anthropic
- D) Native Windows PowerShell installer, because WSL adds unnecessary overhead

**Answer: C**

---

**Q77.** What does the `claude doctor` command do?

- A) It runs health checks on your codebase and suggests code quality improvements
- B) It checks installation integrity, authentication status, system compatibility, and network connectivity to the Claude API
- C) It diagnoses and repairs corrupted CLAUDE.md files
- D) It generates a bug report and sends it to Anthropic support

**Answer: B**

---

**Q78.** According to the content, what happens to a Homebrew installation of Claude Code regarding automatic updates?

- A) Homebrew installations auto-update more frequently than native installs
- B) Homebrew installations do NOT auto-update; you must run `brew upgrade claude-code` manually
- C) Homebrew installations auto-update but only when connected to WiFi
- D) Auto-updates are disabled for all Claude Code installations by default

**Answer: B**

---

**Q79.** What is the key capability that makes Agent Teams in Claude Code valuable for complex business problems?

- A) Agent Teams allow multiple human developers to share a single Claude Code session
- B) Agent Teams allow multiple Claude Code sessions to coordinate, with one session acting as orchestrator delegating specialized subtasks to other sessions running in parallel
- C) Agent Teams provide a shared whiteboard interface for collaborative planning
- D) Agent Teams automatically split billing among multiple team members

**Answer: B**

---

**Q80.** What is "Dispatch" in the Cowork context, and what makes it different from a regular Cowork session?

- A) Dispatch is a keyboard shortcut that sends the current task to a cloud server
- B) Dispatch is a persistent conversation thread in Cowork where Claude remembers context across tasks, allowing you to assign work from your phone that Claude executes on your desktop computer
- C) Dispatch is a feature that delivers Cowork output to your email inbox
- D) Dispatch is a separate subscription tier for enterprise users

**Answer: B**

---

**Q81.** What subscription plan is required to use Dispatch in Cowork?

- A) Free plan is sufficient
- B) Team or Enterprise plan only
- C) Pro or Max plan
- D) Any paid plan including Team and Enterprise

**Answer: C**

---

**Q82.** When does a Dispatch task fail to run on schedule?

- A) When the task description is longer than 500 characters
- B) When your computer is asleep or the Cowork app is closed at the scheduled time; the task queues and fires when the desktop becomes active again
- C) When the task involves file operations rather than web browsing
- D) When two Dispatch tasks are scheduled within 5 minutes of each other

**Answer: B**

---

**Q83.** In Claude Code's Computer Use feature, what determines the "permission tier" for a given application?

- A) The user manually selects a tier (View only / Click only / Full control) for each app in Settings
- B) The tier is fixed by app category — browsers are view-only, terminals are click-only, and most other apps get full control; users cannot upgrade or downgrade a tier
- C) Anthropic assigns tiers through a monthly update based on security research
- D) The tier defaults to full control and users must downgrade manually

**Answer: B**

---

**Q84.** Which hardware requirement is mandatory for Computer Use in Claude Code as of March 2026?

- A) Any Windows 10+ machine with 16GB RAM
- B) Any Linux machine running Ubuntu 22.04 or later
- C) A Mac with Apple Silicon (M1, M2, M3, M4, or later) with a Claude Pro or Max subscription
- D) Any machine with a dedicated NVIDIA GPU

**Answer: C**

---

**Q85.** In the Computer Use tool priority hierarchy, what is the order from HIGHEST to LOWEST priority?

- A) Computer Use → Browser → Bash → Connectors
- B) Connectors → Bash → Browser (Claude in Chrome) → Computer Use (slowest)
- C) Bash → Connectors → Computer Use → Browser
- D) Browser → Computer Use → Connectors → Bash

**Answer: B**

---

**Q86.** What are Cowork "Channels," and what type of automation do they enable?

- A) Channels are communication threads between human team members in Cowork
- B) Channels are event-driven automation pipelines that trigger Cowork tasks when specific events occur (e.g., a file is added to a folder, an email arrives), enabling reactive rather than scheduled automation
- C) Channels are video streaming integrations that connect Cowork to Zoom or Teams
- D) Channels are billing categories that track Cowork usage by project

**Answer: B**

---

**Q87.** According to the Code vs. Cowork Decision Framework, what is the simple primary rule for choosing between the two interfaces?

- A) Use Claude Code if you have a terminal; use Cowork if you prefer a GUI
- B) Use Claude Code if you're on macOS; use Cowork if you're on Windows
- C) Code for code (software development); Cowork for documents (word docs, spreadsheets, PDFs, presentations)
- D) Use Cowork for everything unless you are a senior engineer

**Answer: C**

---

**Q88.** According to the content, what is the key limitation of the xlsx Skill compared to the docx Skill?

- A) The xlsx Skill cannot read existing files, only create new ones
- B) The xlsx Skill does not support tracked changes, while docx does; complex spreadsheets with thousands of formulas or Power Query operations may not preserve perfectly
- C) The xlsx Skill requires a separate MCP server to function
- D) The xlsx Skill is only available on macOS, not Windows

**Answer: B**

---

**Q89.** What is the PDF Skill's key limitation regarding PDFs compared to other built-in Skills?

- A) PDFs cannot be read by Claude at all
- B) The PDF Skill can read and extract content from PDFs but CANNOT create new PDFs or edit existing ones; password-protected PDFs cannot be read
- C) PDFs can only be processed if they are under 1MB in size
- D) The PDF Skill requires OCR software to be installed separately on the user's machine

**Answer: B**

---

**Q90.** In Cowork Projects, what is "Project Memory" and what is its scope?

- A) Project Memory is a cloud database that stores all Cowork sessions globally across all projects
- B) Project Memory allows Claude to retain context from previous tasks within the same project, but memory is scoped per-project — separate projects start fresh with no memory of each other
- C) Project Memory is limited to the last 5 tasks; older memories are automatically deleted
- D) Project Memory requires you to explicitly trigger `/save-memory` after each task

**Answer: B**

---

**Q91.** According to the Cowork Scheduling vs Claude Code Scheduling comparison, what distinguishes Claude Code's `/loop` skill from Cowork Desktop Scheduling in terms of persistence?

- A) `/loop` runs indefinitely while Cowork scheduling has a 3-day auto-expiry
- B) `/loop` is session-scoped (terminates when the session ends) with a 50-task limit and 3-day auto-expiry; Cowork scheduling survives app restarts with no documented task limit or expiry
- C) Cowork scheduling terminates at midnight every day regardless of configuration
- D) Both have identical persistence behavior; the only difference is the interface

**Answer: B**

---

**Q92.** Where do Custom Visuals render, and where do they NOT render, in the Claude product ecosystem?

- A) They render everywhere Claude is available, including API responses
- B) They render in Claude web chat (claude.ai) and Claude Desktop app only; they do NOT render in Cowork sessions, mobile apps, or API responses
- C) They render only in Cowork but not in Claude web chat
- D) They render only through API responses, not in any chat interface

**Answer: B**

---

**Q93.** In the SWE-bench Verified Leaderboard as of March 2026 (cited in the content), which model holds the top position and what is its score?

- A) Gemini 3.1 Pro at 80.6%
- B) GPT-5.2 at 80.0%
- C) Claude Sonnet 4.6 at 79.6%
- D) Claude Opus 4.5 at 80.9%

**Answer: D**

---

**Q94.** What is the Agentic AI Foundation (AAIF) and what is its governance structure?

- A) A private consortium run by Anthropic and OpenAI jointly, with paid membership tiers
- B) A foundation formed under the Linux Foundation on December 9, 2025, with 146 members (as of February 2026) including Anthropic, OpenAI, Google, Microsoft, and AWS; David Nalley (AWS) serves as governing board chair
- C) A government regulatory body overseeing AI agent deployment in enterprises
- D) An academic research institute funded by DARPA to standardize AI agent safety

**Answer: B**

---

**Q95.** In the Digital FTE revenue model described in Chapter 14, what does the "Success Fee" model charge for?

- A) A flat monthly subscription regardless of usage
- B) A one-time license fee for the SKILL.md file
- C) Pay-per-result pricing (e.g., $5 per qualified lead, 2% of cost savings, $50 per document processed)
- D) Hourly consulting rates for building and maintaining the agent

**Answer: C**

---

**Q96.** The content describes three authentication methods for Claude Code. Which method should Console API users NOT use by default, according to the recommendation?

- A) Claude App Authentication (Method 1)
- B) There is no restriction; all three methods are equally recommended
- C) Enterprise Authentication via Bedrock or Vertex AI (Method 3)
- D) Console API Authentication should be avoided if you also have a Claude.ai subscription — use Method 1 (Claude App Auth) instead as it's simpler and provides unified access

**Answer: D**

---

**Q97.** According to the Cross-Vendor Landscape lesson, what percentage of public GitHub commits does Claude Code account for as of early 2026?

- A) 1%
- B) 4%
- C) 10%
- D) 25%

**Answer: B**

---

**Q98.** What is the "Three Roles Framework" described in the CLAUDE.md co-learning section of Chapter 14?

- A) Developer, QA Engineer, and DevOps Engineer working on the same Claude Code session
- B) A collaboration pattern where AI teaches the user (AI as Teacher), the user teaches AI domain knowledge (You as Teacher), and both converge on the best solution together (AI as Co-Worker)
- C) Three different LLM models that review each other's output before final delivery
- D) The roles of Orchestrator, Builder, and Governor in a multi-agent system

**Answer: B**

---

**Q99.** Comparing the "Agent Factory Business Model" for monetizing Skills, which statement correctly describes why Skills are more financially scalable than traditional consulting?

- A) Skills require no ongoing maintenance and generate royalties automatically without any human involvement
- B) Unlike hourly consulting (sell time once), a Skill is encoded expertise sold repeatedly — create once, sell thousands of times, serve unlimited customers simultaneously without additional labor cost
- C) Skills are tax-exempt in most jurisdictions, making them more profitable
- D) Skills can be patented and licensed through traditional IP law, providing exclusive market rights

**Answer: B**

---

**Q100.** According to the content, which of the following best distinguishes when to use Claude Code versus Cowork for a hybrid workflow involving data analysis and stakeholder presentation?

- A) Use Cowork for everything, since it has both coding and document capabilities
- B) Use Claude Code to write and debug the Python analysis scripts and run Jupyter notebooks; use Cowork to create the stakeholder report as a formatted document and distribute it via browser integration — each interface handles what it's optimized for
- C) Use Claude Code for all steps because it has a larger context window than Cowork
- D) Use Cowork for data analysis and Claude Code for document creation, as Cowork handles raw data better

**Answer: B**

---

*End of 100 MCQs — General Agents Foundations (Across 12, 13, 14)*
