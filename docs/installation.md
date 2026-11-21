# Installation and compatibility

StylePort contains standard Agent Skills. Each skill is a directory with a `SKILL.md` file and optional `references/`, `scripts/`, and `assets/` resources.

## Skills CLI

The repository is intended to be installable as a public skill collection:

```bash
npx skills add MaduroLabs/styleport
```

Do not install a release into a production project as an unreviewed side effect. Review the downloaded skill files first, then pin a release or commit when reproducibility matters.

## Codex

Project-scoped skills belong under:

```text
.agents/skills/<skill-name>/SKILL.md
```

User-scoped skills belong under `~/.agents/skills/<skill-name>/SKILL.md`.

The skills can be invoked by name, for example:

```text
Use frontend-style-extractor to document this frontend.
Use frontend-style-adapter to apply design-system/portable/.
```

## Claude Code

Project-scoped skills belong under:

```text
.claude/skills/<skill-name>/SKILL.md
```

Invoke them with `/frontend-style-extractor` or `/frontend-style-adapter`.

## Cursor

Cursor's native project path is:

```text
.cursor/skills/<skill-name>/SKILL.md
```

Cursor also supports the shared `.agents/skills/` layout. Invoke a skill with `/frontend-style-extractor` or `/frontend-style-adapter`, or let the agent select it from the description.

## Resource paths

Scripts are relative to the skill directory. If a client does not provide a skill-root variable, resolve the directory containing `SKILL.md` before running:

```bash
python3 <skill-root>/scripts/validate_bundle.py <bundle-path>
python3 <skill-root>/scripts/style_inventory.py <source-root>
```

The scripts use Python 3.9+ standard-library features and do not require a package installation.
