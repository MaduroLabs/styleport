# Adapter mapping playbook

## Mapping source design intent into target technology

| Source | Target | Approach |
| --- | --- | --- |
| CSS variables | CSS/SCSS/CSS Modules | Define semantic tokens at target theme root and update shared components to reference them. |
| Tailwind v3 theme config | Tailwind v3 | Map into existing `tailwind.config.*` theme extension; respect target aliases and dark mode strategy. |
| Tailwind v4 `@theme` | Tailwind v4 | Add compatible CSS tokens under existing theme strategy; inspect actual target v4 setup before edit. |
| CSS-in-JS/theme provider | MUI/styled-components/Emotion | Update established theme object/providers; do not add redundant theme systems. |
| Any source stack | Vue/Svelte/React/Next.js | Migrate semantic tokens and component contracts, not source hooks, imports, routing or component implementations. |

## Decision for each rule
- `apply`: target surface has same semantic role; rule compatible and observed.
- `adapt`: target has analogous function but needs different layout/responsive behavior; explain change.
- `skip`: out of requested scope, source-specific ornament, or missing target surface; record why.
- `blocked`: needs an inaccessible source asset/font, unsafe library change, conflicting requirement, or unknown theme behavior; do not guess.

## Typical order
1. Base/background/text/focus colors + typography and typography fallback.
2. Spacing/radius/shadow, containers and density scale.
3. Shared button/input/link/card/alert/table variants; protect `aria-*` and event handling.
4. Dashboard/menu/layout and page-specific patterns.
5. Desktop/tablet/mobile and visual states; avoid desktop-only overflow.
6. Build/typecheck/test, keyboard navigation and screenshot comparison where possible.

## Safety gates
- Keep existing API boundaries, routing contracts, analytics data attributes, form names and test IDs.
- Use smallest workable diff, preserve uncommitted work; avoid edits to generated output.
- Avoid global regex replacement of colors; check source selectors/usage because the same hex may mean different semantics.
- If missing source font/asset rights, choose licensed equivalent or fallback and report trade-off.
- Respect target's accessibility, contrast and reduced-motion support over reference visual similarity.
- Check dark mode and user theme preference if target supports it.

## Verification report shape
- Scope: routes/components inspected and updated.
- Mapping: token names → target implementation files; counts `apply/adapt/skip/blocked`.
- Validation: command, exit status, and failures; rendered viewports actually inspected.
- Behavior: tests or manual checks performed; unresolved regressions/risks.
- Remaining items: concrete follow-up tasks, not generic promises.
