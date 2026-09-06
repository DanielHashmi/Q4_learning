# Harness Engineering Projects

A practical progression through **agent harness design**: constrain what an agent can do, make failures observable, verify outcomes independently, and turn each lesson into a durable contract.

## Project map

| Project | Focus | What it demonstrates |
| --- | --- | --- |
| [01 · First Wall](./01-first-wall/) | Permissions | Default-deny behavior and tool-level boundaries can block secret reads and destructive actions. |
| [02 · Lint Hook](./02-lint-hook/) | Enforcement | Post-edit, stop, and pre-commit hooks catch broken code without relying on agent memory. |
| [03 · Error Audit](./03-error-audit/) | Recoverability | Specific, actionable error messages enable deterministic recovery; vague errors produce flailing. |
| [04 · Tool Diet](./04-tool-diet/) | Tool surface | A real HTTP backend and independent verifier compare overlapping and lean tool manifests. |
| [05 · Typed Reviewer](./05-typed-reviewer/) | Contracts | A schema-validated reviewer accepts only `PASS` or `FAIL`; malformed verdicts escalate. |
| [06 · Ratchet Week](./06-ratchet-week/) | Learning loops | Real failures are classified and fixed on the surface where they occurred. |
| [07 · Fenced Night](./07-fenced-night/) | Unattended safety | A prompt-injection attempt is contained, disclosed, and escalated when review is unavailable. |
| [08 · Model Swap](./08-model-swap/) | Portability | The hardened loop is exercised across OpenCode/Gemini and a Claude Code/Claude scaffold. |

## The progression

```text
permissions → hooks → errors → tools → typed review → ratchets → unattended runs → model portability
```

Each directory contains a results-oriented README and, where applicable, a small runnable `repo/` that makes the experiment concrete. The projects favor **mechanical evidence**—exit codes, logs, schemas, independent state checks, and explicit escalation—over claims that an agent will behave correctly because it was asked nicely.

## Start here

Read the projects in numerical order for the intended progression. For a focused entry point, begin with [01 · First Wall](./01-first-wall/) to see permission boundaries in action, then compare it with [05 · Typed Reviewer](./05-typed-reviewer/) for protocol-level verification.

> These projects are learning experiments and test harnesses. Secret material referenced by the experiments is synthetic and intended for testing only.
