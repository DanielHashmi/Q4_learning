# 🌱 What is Spec Kit Plus?

**Spec Kit Plus** is a development toolkit that transforms how you build software with AI—by writing specifications instead of code.

 AI coding assistants are powerful, but without structure they produce inconsistent results and accumulate technical debt. Spec Kit Plus solves this by treating natural language specifications as your primary source of truth, with AI agents "compiling" them into production code.

---

## ⚙️ How It Works

Spec Kit Plus brings together three core components:

- 📝 **Markdown specifications** (`spec.md`, `plan.md`, `tasks.md`) - what you write to describe your software
- 🤖 **AI CLI agents** (Gemini, Claude, Qwen, etc.) - these read your specs and generate code
- 🔧 **Workflow commands** (`/sp.specify`, `/sp.plan`, `/sp.tasks`, `/sp.implement`) - structured steps that guide development

Once set up, you describe features in plain English, and AI agents handle the implementation—with built-in quality gates through Test-Driven Development.

---

## ✨ What You Can Build

Here are real examples of what becomes possible:

- 🏗️ **Full-stack applications** - Describe a Kanban board app, AI generates the database schema, API, and UI
- 🔄 **Multi-agent systems** - Build distributed AI systems with standardized protocols (MCP, A2A)
- 📦 **Cloud-native services** - Deploy to Kubernetes with Docker, Dapr, and Ray automatically
- 🧪 **Test-driven features** - Every implementation comes with comprehensive test coverage

---

## 🎯 Why This Matters

### 👤 If you're a developer:

You transition from writing code to writing specifications—focusing on **what to build** and **why**, while AI handles the **how**. Your role evolves to system architect and specification engineer.

### 👨‍💻 If you lead engineering teams:

You get **2-3× faster delivery** with **50% fewer bugs** because specifications prevent the architectural drift and technical debt that plague "vibe coding" approaches.

---

## 🧱 The Five Core Workflow Phases

Spec Kit Plus structures development into clear phases:

| Phase | Command | What It Does |
|-------|---------|-------------|
| 📜 **Constitution** | `/sp.constitution` | Establish project standards and principles |
| 📋 **Specification** | `/sp.specify` | Define feature requirements and acceptance criteria |
| 🏗️ **Planning** | `/sp.plan` | Design technical architecture and tech stack |
| ✅ **Tasks** | `/sp.tasks` | Break implementation into testable units |
| 🚀 **Implementation** | `/sp.implement` | Execute tasks with TDD (Red-Green-Refactor) |

---

## 🚀 Getting Started

Spec Kit Plus is **open source** and supports **13 AI coding agents** including Claude, Gemini, Cursor, and GitHub Copilot.

Install with a single command:

```bash
pip install specifyplus  
specifyplus init my-project --ai claude
```