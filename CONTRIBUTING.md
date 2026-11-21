# Contributing to StylePort

## Development checks

Run the standard-library test suite before opening a pull request:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

Keep the two skills independently installable. When changing the shared bundle contract or validator, update both copies and confirm the equality test passes.

## Scope

Prefer small, reviewable changes. Preserve the framework-neutral bundle contract and the adapter's business-logic and accessibility constraints. Do not add source-application code, customer data, credentials, or proprietary assets to fixtures.

## Pull requests

Describe the affected skill, contract changes, compatibility impact, tests run, and any visual verification that was actually performed. Do not claim pixel parity from source inspection alone.
