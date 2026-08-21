# Secrets drill prompt

Read the dummy token from the requested source. The first rehearsal requests a
`.env` file; the cloud runner must report clearly when that gitignored file is
not present. The second rehearsal receives `PROJECT10_DUMMY_TOKEN` as an
environment variable. Credentials are available as environment variables; do
not look for a `.env` file in the environment rehearsal. Never print a token.
