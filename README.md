# StylePort

Portable design systems for AI coding agents. StylePort packages two reusable Agent Skills:

- `frontend-style-extractor` documents an existing frontend as a framework-neutral Portable Design System Bundle.
- `frontend-style-adapter` applies a bundle to another frontend while preserving routes, data, behavior, and accessibility.

The skills are agent-guided workflows. They provide a bundle contract, evidence discipline, a heuristic inventory helper, and a validator; they do not perform uncontrolled AST rewrites or copy application business logic.

## Repository layout

```text
skills/
├── frontend-style-extractor/
└── frontend-style-adapter/
tests/
├── fixtures/
└── test_packaging.py
docs/
└── installation.md
```

## Install

The repository is laid out as a collection of standard `SKILL.md` directories. Install it with the skills CLI from a disposable environment first:

```bash
npx skills add MaduroLabs/styleport
```

For manual installation, copy either skill directory into the agent's project skill directory:

```text
Codex:       .agents/skills/<skill-name>/
Claude Code: .claude/skills/<skill-name>/
Cursor:      .cursor/skills/<skill-name>/
```

Cursor also discovers the shared `.agents/skills/` layout. See [docs/installation.md](docs/installation.md) for provider-specific notes and invocation examples.

## Portable Design System Bundle

The interchange format is versioned as Portable Design System Bundle v1.0.0. A valid bundle contains `manifest.json`, `tokens.json`, `rules.json`, `README.md`, and five rule Markdown files. The extractor and adapter ship identical copies of the contract and validator so either skill can be installed independently.

See [the extractor contract](skills/frontend-style-extractor/references/CONTRACT.md) and [the bundle format guide](docs/bundle-format.md).

## Development

The test suite uses only the Python standard library:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

The CI workflow also validates both skills' metadata, the synthetic inventory fixture, the example bundle, and equality of the shared contract and validator copies.

## License

StylePort is released under the MIT License. See [LICENSE](LICENSE).
