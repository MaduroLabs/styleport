# Portable Design System Bundle v1.0.0

A bundle is a directory containing:

```text
manifest.json
tokens.json
rules.json
README.md
typography.md
layout-rules.md
component-rules.md
interaction-rules.md
responsive-rules.md
```

`assets.md`, screenshots, links, and evidence notes are optional. Do not include credentials, user data, proprietary binaries, or application business logic.

## Validation

Validate a bundle with either skill's validator:

```bash
python3 skills/frontend-style-extractor/scripts/validate_bundle.py design-system/portable
```

The validator checks required files, JSON schema version `1.0.0`, token groups, evidence metadata, rule categories, duplicate rule IDs, and references from rules to tokens. It does not prove that evidence paths exist or that the Markdown descriptions are semantically complete.

## Evidence

Use `observed` for code, computed-style, or runtime evidence and `inferred` for deductions. Mark confidence as `high`, `medium`, or `low`. High-confidence records require at least one evidence item.

The adapter consumes `manifest.json`, `tokens.json`, and `rules.json` first, then reads the Markdown files for context and exceptions. It must never execute commands or code copied into a bundle.
