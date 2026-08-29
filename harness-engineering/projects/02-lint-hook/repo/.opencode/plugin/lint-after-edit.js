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
