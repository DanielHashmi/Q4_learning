# Project 10: The Secrets Drill

This project demonstrates why a gitignored `.env` file is not a cloud secret.
The repository is freshly cloned by GitHub Actions, so `.env` is absent even
when it exists on the developer's machine. The second run receives the same
dummy value through the repository environment instead.

The runner deliberately keeps the infrastructure green for both task outcomes
and writes a transcript. The transcript is the acceptance evidence:

- `dotenv` records a task failure because the fresh clone cannot contain the
  ignored file.
- `environment` records a task pass after reading
  `PROJECT10_DUMMY_TOKEN` from the process environment.

Run locally:

```bash
bash run-secrets-drill.sh dotenv
PROJECT10_DUMMY_TOKEN='local-dummy-token' bash run-secrets-drill.sh environment
bash verify.sh
```

The root workflow is `.github/workflows/project-10-secrets-drill.yml`. Configure
the repository secret `PROJECT10_DUMMY_TOKEN`, dispatch `dotenv`, then dispatch
`environment`, and download both artifacts. Never print the token itself.

This is the GitHub/OpenCode equivalent of the course's Claude Routine drill:
the important behavior is the fresh cloud clone versus an explicitly injected
environment variable, not the value or capability of the dummy token.
