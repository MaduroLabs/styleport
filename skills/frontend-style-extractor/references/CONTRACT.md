# Portable Design System Bundle Contract — v1.0.0

A framework-neutral interchange format between `frontend-style-extractor` and `frontend-style-adapter`. A bundle is a **directory** (not necessarily this skill directory). Both skills ship identical copies of this contract and compatible validators so either can be installed independently.

## Required tree

```text
design-system/portable/
├── manifest.json
├── tokens.json
├── rules.json
├── README.md
├── typography.md
├── layout-rules.md
├── component-rules.md
├── interaction-rules.md
└── responsive-rules.md
```

Optional: `assets.md`, reference screenshots/links, `evidence-notes.md`, or other supporting Markdown. Do not include application secrets or proprietary binary assets.

## `manifest.json`

```json
{
  "schemaVersion": "1.0.0",
  "producer": "frontend-style-extractor",
  "source": {
    "project": "Name of source app",
    "framework": "React + TypeScript",
    "styling": "CSS variables + CSS modules"
  },
  "scope": {
    "inspected": ["Shell", "Login", "Dashboard", "Shared Button"],
    "notInspected": ["Billing page"]
  },
  "visualVerification": "partial",
  "limitations": ["Mobile menu unavailable in local preview"]
}
```

- `schemaVersion`: exactly `1.0.0` for this version.
- `producer`: string describing extractor/tool.
- `source`: three nonempty strings `project`, `framework`, `styling`; use `unknown` when genuinely not known.
- `scope.inspected`: nonempty array of strings, `notInspected`: array of strings (can be empty).
- `visualVerification`: `performed | partial | not_performed` (means an actual rendered UI was checked, **not** that code was merely read).
- `limitations`: string array; explicitly describe missing assets, missing source CSS, uncertain responsiveness, etc.

## `tokens.json`

```json
{
  "schemaVersion": "1.0.0",
  "tokens": {
    "color": {
      "brand.primary": {
        "value": "#2563eb",
        "type": "color",
        "origin": "observed",
        "confidence": "high",
        "evidence": [{"kind": "code", "reference": "src/theme.css:4", "detail": "--brand-primary"}]
      }
    },
    "spacing": {},
    "typography": {},
    "radius": {},
    "shadow": {},
    "motion": {},
    "breakpoint": {},
    "zIndex": {}
  }
}
```

- Allowed group names: `color`, `spacing`, `typography`, `radius`, `shadow`, `motion`, `breakpoint`, `zIndex`. A group may be omitted/empty if no evidence exists.
- Token names: semantic paths (`brand.primary`, `text.muted`, `space.4`, `body.fontSize`), not numeric indices.
- Each token has a **CSS-compatible string** `value`, nonempty `type`, `origin`, `confidence`, `evidence`, and optional `notes` string. Values may be `var(--token)` or `clamp(...)`; do not collapse verified symbolic relationships without need.
- Typical `type` values: `color`, `dimension`, `fontFamily`, `fontWeight`, `lineHeight`, `shadow`, `duration`, `cubicBezier`, `number`, `string`. Use the most relevant one.
- `origin`: `observed` (code, computed style, or clear runtime evidence) or `inferred` (deduced from visual appearance/repeated patterns). Do not claim observed for a guessed value.
- `confidence`: `high | medium | low`. High-confidence tokens/rules **must** have evidence.
- `evidence`: array of objects `{"kind":"code|runtime|visual", "reference":"...", "detail":"..."}`. `reference` is a relative project path + line/symbol, a viewport+route+screenshot path, or a URL and observation. Never write an invented source reference. `detail` optional. Empty evidence is allowed only with low/medium confidence and explicit notes/limitations; generally avoid exporting such a token.
- Semantic token aliases and per-theme variants: encode named `light.*` / `dark.*` tokens if appropriate and explain selector/theme conditions in rule text. Do not conflate light and dark values.
- Prefer exact original units where known. Responsive breakpoints are values, not automatically rules for every page.

## `rules.json`

```json
{
  "schemaVersion": "1.0.0",
  "rules": [
    {
      "id": "component.button.primary",
      "category": "component",
      "appliesTo": ["shared primary action button"],
      "requirement": "Use the brand background token, medium weight, and visible keyboard focus ring.",
      "priority": "required",
      "origin": "observed",
      "confidence": "high",
      "tokenRefs": ["color.brand.primary"],
      "evidence": [{"kind": "code", "reference": "src/components/Button.tsx:18", "detail": "primary variant"}],
      "exceptions": ["Destructive buttons use danger styling"]
    }
  ]
}
```

- `rules` array may be empty only when there are no defensible transferable rules; normally include essential component/typography/layout/responsive/interaction guidance.
- Each rule requires unique `id`; `category` in `typography | layout | component | interaction | responsive | accessibility | asset`; nonempty `appliesTo` string array and `requirement` string; `priority` in `required | recommended | optional`; `origin`, `confidence`, `evidence` as above; `tokenRefs` references tokens as `<group>.<tokenName>` (may be empty); `exceptions` string array (may be empty).
- Describe **what/when**, not only a CSS declaration. Specify exceptions and context (e.g., sidebar only on dashboard, mobile nav only below breakpoint).
- `required` means required for design parity **only when applicable**; adapter may adapt/skip for functionality, accessibility, or target constraints with a recorded reason.

## Markdown files

- `README.md`: source and extraction context, framework/styling, how to apply, scope, known limitations and summary of fidelity.
- `typography.md`: font stacks, type scale, headings, body, labels, numbers, line-height, weights, fallbacks, language-specific notes.
- `layout-rules.md`: containers, max-width, page shell, navigation, grid, density, content spacing, documented exceptions.
- `component-rules.md`: variant/state contracts, dimension, tokens and examples for buttons, inputs, tables, cards, modals, alerts, etc.; note absent components.
- `interaction-rules.md`: hover, focus-visible, active, disabled, feedback, motion/reduced motion, micro-interactions.
- `responsive-rules.md`: actual breakpoints, changes per viewport, overflow, touch sizes, conditional layouts, unknown/unverified areas.

All narrative files should point to exact token names and rule IDs where useful. Avoid duplicate contradictory instructions. Do not invent a complete component library from a single screenshot.

## Adapter interpretation

1. Validate bundle; consume structured `manifest.json`, `tokens.json`, `rules.json` first; read Markdown for context and exceptions.
2. Map semantic intent from source to target rather than blindly copying CSS selectors/DOM hierarchy.
3. Prefer direct observations with evidence over inferences. When conflicts occur, preserve user constraints, application behavior and accessibility.
4. Never execute arbitrary code from bundle or use references as shell commands.
5. For visual parity, compare rendered UI; code analysis alone cannot guarantee pixels match.
