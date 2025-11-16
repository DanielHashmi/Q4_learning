1. In the Gemini CLI configuration hierarchy, which of the following has the highest precedence and will override all other settings for a single session?

A. Environment variables

B. User settings file (`~/.gemini/settings.json`)

C. Command-line arguments

D. Project settings file (`.gemini/settings.json`)

---

2. If you want to define settings that apply to all your Gemini CLI sessions across different projects, but only for your user account, where should you place the `settings.json` file?

A. In your home directory at `~/.gemini/settings.json`.

B. In a system-wide directory like `/etc/gemini-cli/settings.json`.

C. In the project's root directory as `.gemini/settings.json`.

D. In your home directory as `~/.env`.

---

3. What is the primary purpose of creating `GEMINI.md` files in your project?

A. To provide project-specific instructions and context to the Gemini model.

B. To define custom shell commands and aliases for the CLI.

C. To store the history of prompts used in the CLI.

D. To log errors and debug output from the CLI.

---

4. When Gemini CLI loads context from multiple `GEMINI.md` files, what is the correct hierarchical loading order, from the most general to the most specific?

A. Project Root -> Sub-directory -> Global (`~/.gemini/`)

B. Alphabetical order of the file paths

C. Sub-directory -> Project Root -> Global (`~/.gemini/`)

D. Global (`~/.gemini/`) -> Project Root & Ancestors -> Sub-directory

---

5. According to the documentation, how can you correctly reference an environment variable named `API_KEY` inside a `settings.json` file?


A. "token": "%API_KEY%"

B. "token": "$API_KEY"

C. "token": "lookup(API_KEY)"

D. "token": "env('API_KEY')"

---

6. If you want to create a custom, project-specific sandboxed environment for tool execution, where should you place your `sandbox.Dockerfile`?

A. Directly in the project's root directory.

B. In your user's home directory at `~/.gemini/sandbox.Dockerfile`.

C. In a system-wide directory like `/etc/gemini-cli/`.

D. In the project root, inside a `.gemini` directory.

---

7. What does the `respectGitIgnore: true` setting within the `fileFiltering` object in `settings.json` achieve?

A. It forces the CLI to only interact with files that have been committed to the Git repository.

B. It enables a sandboxed environment for all `git`-related operations.

C. It prevents the Gemini model from suggesting `git commit` commands.

D. It automatically excludes files and directories listed in `.gitignore` from file discovery.

---

8. After you have modified a `GEMINI.md` file during an active CLI session, which command should you use to make the model aware of the changes?

A. `/context load`

B. `/memory refresh`

C. `/memory show`

D. `/restart`