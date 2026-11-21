# Style adoption plan

## Target and reference
- Target repo / branch:
- Bundle path and source project:
- Scope / excluded pages:
- Git worktree status before edits:
- Constraints / existing styling stack:

## Token mapping
| Reference token | Target semantic token or implementation file | Action | Reason |
|---|---|---|---|
| `color.brand.primary` | `src/styles/theme.css` / `--color-primary` | apply | Equivalent role |

## Component and rule mapping
| Rule ID | Target files / components | Decision (apply/adapt/skip/blocked) | Constraints / verification |
|---|---|---|---|
| `component.button.primary` | `src/components/Button.tsx` | apply | Check focus, disabled and button submission |

## Implementation order
1. Theme tokens / typography.
2. Shared presentation primitives.
3. Page shell and scoped screens.
4. Interaction, responsiveness, reduced motion and regressions.

## Verification checklist
- [ ] Typecheck / lint / unit tests (record commands and results)
- [ ] Build and representative route smoke tests
- [ ] Mobile / tablet / desktop views if browser exists
- [ ] Focus, hover, disabled, errors and keyboard accessibility
- [ ] Theme/contrast checks; visual comparison only if actually performed

## Deviations, blocked work and rationale
-

## Final outcome
- Files changed:
- Rule decisions (apply/adapt/skip/blocked):
- Commands and observed results:
- Known defects / remaining work:
