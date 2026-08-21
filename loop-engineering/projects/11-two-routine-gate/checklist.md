# Project 11 A6 safety checklist

- Success condition: A produces a draft PR; B writes one follow-up record only after approval.
- Limit: one draft and one follow-up per workflow run; no schedules or loops.
- Isolation: A and B require the `claude/project-11-draft-*` branch namespace.
- Checker: the human reviews A's draft; B rechecks its markers before acting.
- State: `progress.md` is committed with draft and follow-up state.
- Human gate: A cannot execute; B requires an approval note in the API request.
- Log: both workflows upload complete transcript artifacts.
- Connectors: only GitHub Actions and the explicitly fired GitHub API workflow are used.
- Identity: the B bearer token is a repository secret and is never emitted.
