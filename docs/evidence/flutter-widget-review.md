# Evidence: flutter-widget-review

Status: removed after A/B test, no measurable benefit over the agent without the skill.

Tested 2026-10-27 on XE-Rate at app `main` commit `d544e1a`. Four independent Git worktrees were created from that commit. The two “with” worktrees received the corrected skill. Flutter 3.47.7, Dart 3.13.5.

## Method

Two independent pairs of agent runs used the same review task and rules. Each run inspected `lib/`, reported findings, applied up to three selected fixes, ran `dart format` and `flutter analyze`, and saved its findings and diff under `C:\Users\abduk\Documents`. A separate reviewer opened the cited source locations in each baseline worktree and classified the claims. No commits were made; app `main` remained at `d544e1a`.

## Results

| Run | Findings (REAL / FALSE / UNSURE) | Fixes applied | Changed app files | Analyzer |
|---|---:|---|---:|---|
| Without skill, 1 | 6 / 0 / 0 | Async mounted guards and `PageController.dispose()` | 5 | 5 pre-existing issues; exit 1 |
| With skill, 1 | 5 / 0 / 0 | Async mounted guards | 3 | 5 pre-existing issues; exit 1 |
| Without skill, 2 | 7 / 0 / 0 | Async mounted guards, `PageController.dispose()`, scrollable exchange form | 5 | 5 pre-existing issues; exit 1 |
| With skill, 2 | 6 / 0 / 0 | Async mounted guards and `PageController.dispose()` | 3 | 5 pre-existing issues; exit 1 |

The shared findings were asynchronous `setState` calls without mounted checks, an undisposed `PageController`, and a possible vertical overflow in the exchange form. Run 2 without the skill also reported extra layout work from `IntrinsicHeight`. The independent reviewer confirmed each reported positive finding against the baseline source. No deprecated API problem was found.

All four analyzer runs reported the same pre-existing problems: two naming infos in `lib/api/currency_api.dart`, a missing `api_keys.dart` import and undefined `YOUR_SECRET_API` in `lib/api/exchange_api.dart`, and an `avoid_print` info in `lib/currency/currency.dart`. Formatter checks completed. The saved diffs match the final tracked worktree diffs; the injected `.github/` skill in “with” worktrees is not an app edit.

## What the skill changed

- Both with-skill runs fixed fewer of the confirmed issues than their paired runs without the skill.
- The main findings appeared in both conditions; the skill did not reveal a unique confirmed issue.
- Across two pairs, the skill showed no repeatable improvement. This small test does not establish a general performance difference.

## What this test did not show

- No app was rendered and no visual comparison was performed.
- Two pairs are a small sample; agent-to-agent variation can explain differences in the number of findings and selected fixes.
- `flutter analyze` could not pass because of the existing API-key import/placeholder errors and lint infos.

## Problems found and edits

- The skill’s `shrinkWrap` claim was corrected: it does not force layout of every item; shrink-wrapping is more expensive because the scroll extent must be recomputed as the scroll position changes.
- The `Expanded` rule was corrected: it may have `StatelessWidget` or `StatefulWidget` ancestors; it need not be a direct child.
- Lifecycle and async guidance was narrowed to resources owned by `State` and mounted checks after async gaps.
- The opacity advice was narrowed to directly animating `Opacity.opacity`.
- The unsupported `Color.withOpacity` version was removed; it was not listed in Flutter’s breaking-changes index. `withOpacity` is deprecated in favor of `withValues`.
- After the A/B runs, the `ColorScheme.background` replacement row was updated with the official `3.22.0` stable release for the new Material 3 color roles. This release-note detail does not change the behavior tested in the runs.
- Unsupported generic advice about device-specific dimensions was deleted. Nested-`Container` advice now points to the relevant Dart lints. The `Navigator.push` advice was replaced with the sourced rule that `build()` should have no side effects.
- The A/B results did not show a meaningful benefit. Verdict: **DELETE**. The README Verified cell was not changed. The edited skill remains available for the user to remove or revise.
