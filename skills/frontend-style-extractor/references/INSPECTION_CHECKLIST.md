# Extractor inspection checklist

Use this as a systematic inspection guide, not a requirement to invent absent UI patterns.

## Source discovery
- [ ] `package.json`/lockfiles and styling dependencies (Tailwind, CSS Modules, Sass, UI libraries, CSS-in-JS).
- [ ] Theme configuration, CSS variable definitions, font imports and local font licensing.
- [ ] App shell, navigation, route structure; inspect representative shared/feature components.
- [ ] Existing `AGENTS.md` / project instructions; respect files beyond permitted scope.
- [ ] Check colors/fonts assigned by component variants, not merely global variables.

## Design primitives
- [ ] Semantic palette (brand, neutral, success, warning, danger, backgrounds, text, borders, focus) in each supported theme.
- [ ] Typography: font family, stack/fallback, body/heading sizes, weights, line heights, tracking, text transforms.
- [ ] Spacing and sizing scale: units, container widths, borders, rounding, shadows, elevations, z-index.
- [ ] Transitions/durations/easings, icon sizing, breakpoints, reduced-motion behaviors.

## Shared components and states
- [ ] Navigation/app shell, sidebar, menus, breadcrumbs, tabs, pagination.
- [ ] Button/link variants, inputs, selects, checkbox/radio, field labels, validation/errors.
- [ ] Cards, lists, data tables, tooltips, modals/drawers, notifications/toasts.
- [ ] Hover/active/focus-visible/disabled/loading/empty/error states.
- [ ] High-contrast or dark themes and token overrides if present.

## Responsive and visual verification
- [ ] Observe at narrow/mobile, tablet, desktop widths when browser exists.
- [ ] Note actual CSS breakpoints and which UI changes at each.
- [ ] Verify sticky/fixed elements, scroll/overflow, touch targets and long content.
- [ ] Note visual-only evidence clearly: route, viewport, screenshot reference, environment.

## Evidence hierarchy and interpretation
1. Verified runtime computed styles + component code = strongest for current rendered behavior.
2. Theme definitions/config = strong for intended shared tokens; verify application when possible.
3. Repeated component/pattern usage = moderate evidence for design convention.
4. A single page or visual screenshot = possible exception; do not generalize without support.
5. Guess by eye = inferred/low unless independently checked.

## Export discipline
- Group semantic tokens by purpose. Keep true aliases if defined. Avoid exporting every incidental inline number.
- Keep source-specific branding/photography, copy and licensed font assets out of the export unless authorized.
- Every rule names its applicability/exception and evidence; avoid unsupported universal language.
- Explicitly label unverified states and skipped routes.
- The optional scanner is heuristic and may miss dynamic CSS, Tailwind generated classes, JS theme objects, media-query nesting and computed cascade. It never replaces targeted code inspection.
