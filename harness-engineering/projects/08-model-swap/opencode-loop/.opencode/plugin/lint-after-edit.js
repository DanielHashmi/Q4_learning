// Identical pattern to Project 2's real PostToolUse-equivalent plugin:
// after every edit/write, run the real lint and feed a failure back to
// the agent's next turn as forward-only feedback (it cannot undo the edit).
export const LintAfterEdit = async ({ $ }) => ({
  "tool.execute.after": async (input, output) => {
    if (input.tool === "edit" || input.tool === "write") {
      const result = await $`npm run lint --silent`.nothrow();
      if (result.exitCode !== 0) {
        output.output += "\n[lint] failed:\n" + result.stderr.toString();
      }
    }
  },
});
