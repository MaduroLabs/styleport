---
name: frontend-style-extractor
description: Extract and document a portable frontend design system from an existing web app or accessible website. Use when asked to analyze UI styles, design tokens, typography, layouts, components, interactions, responsiveness, or generate reusable style rules for other projects. Does not redesign, modify, or migrate the source app.
---

# Frontend Style Extractor

## Objective
Produce an evidence-backed, framework-neutral **Portable Design System Bundle v1.0.0** from a source frontend. The output is a handoff contract for `frontend-style-adapter`, NOT copied source code and NOT a pixel-perfect clone.

Read `references/CONTRACT.md` before writing the bundle. Read `references/INSPECTION_CHECKLIST.md` while inspecting. Do not invent style values or represent inferred patterns as observed facts.

## Inputs
- Source: repository root / workspace, selected directories, or an accessible rendered website.
- Optional: specific pages/components, themes, breakpoints, design fidelity, output path.
- Defaults: source = current repository; scope = representative shared UI + routes/pages discoverable in the repository; output = `design-system/portable/` within source repository (unless user requests another location).
- A public URL without accessible source CSS or computed styles is a **visual-only source**. Mark exact pixel/color/spacing measurements as inferred unless measurable via tools. If the environment cannot open the website, explain the limitation instead of fabricating analysis.

## Workflow
1. **Orient without changing source.** Check git status, project structure, package manifest, framework and styling stack, route/page structure, global styles, theme providers, component libraries and design tokens. Respect `AGENTS.md` and repository instructions. Never read `.env`, secrets, or irrelevant data.
2. **Run the optional heuristic inventory** (stdlib-only; not an authoritative CSS parser):
   `python3 <skill-root>/scripts/style_inventory.py <source-root> --out <temporary-path>/style-inventory.json`
   Use a temporary path outside the repository if possible. Read the summary; verify important claims directly in code/rendered UI.
3. **Sample representative UI:** global shell, navigation, headings/text, buttons, fields/forms, cards, tables, modals, alerts, loading/empty/error states; inspect desktop and mobile, hover/focus/disabled, light/dark if supported. Sample both common and unusual routes. Record inspected vs skipped surfaces.
4. **Resolve rule hierarchy:** explicit tokens/configuration → shared components → repeated page patterns → one-off exceptions. Do not mistake a single page's layout for a global rule. Preserve semantic tokens and aliases (e.g. `var(--brand-primary)`) when meaningful; state actual resolved values only if verified.
5. **Record provenance:** each token and each structured rule needs `origin`, `confidence`, and concrete `evidence`. Prefer file path + line/symbol, computed-style observation, or screenshot/viewport reference. Every unsupported inference must be labeled as such. State any limitations, uninspected pages, dependency/asset licensing uncertainty.
6. **Author bundle** at chosen output path. Required files: `manifest.json`, `tokens.json`, `rules.json`, `README.md`, `typography.md`, `layout-rules.md`, `component-rules.md`, `interaction-rules.md`, `responsive-rules.md`. Optional `assets.md` for icon/image/font considerations. See `references/CONTRACT.md` and `assets/example-bundle/` for shape; replace ALL example content with source-specific observations. Use portable language (component contracts and design intent) rather than framework-specific implementation as the only description.
7. **Validate:** `python3 <skill-root>/scripts/validate_bundle.py <bundle-path>`. Fix all errors. Inspect unknown/low-confidence items manually. Do not claim visual fidelity was tested if no browser/screenshot comparison was performed.
8. **Report:** source and surfaces inspected, framework/styling method, output path, token/rule counts, coverage/uncertainties, validator result, and handoff usage: invoke `frontend-style-adapter` with the design system path.

## Hard constraints
- Extract **design language**, not business logic, copy, proprietary assets or implementation internals.
- Do not modify app source, install packages, rewrite configuration, or automatically commit. Creating the requested bundle is allowed.
- Do not copy logos, font binaries, licensed images/icons into the bundle unless user explicitly authorizes and rights are clear; instead describe their appearance, original references, and licensing caveats.
- Do not transfer `.env`, credentials, user data, live API responses, or secrets.
- Preserve separate dark/light themes and responsive rules if they exist; do not flatten into a single style.
- Exact implementation details belong in `evidence`/notes; requirements should remain cross-framework portable.
- Prefer clarity to volume: high-value documented patterns beat hundreds of unsupported tokens.
- If no runnable UI/browser is available, report `visualVerification: "not_performed"` in the manifest.

## Done when
Bundle validates; every exported fact is traceable; global rules are separated from exceptions; accessibility/responsive states are addressed; and the report states known gaps.
