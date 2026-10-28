# Evidence: flutter-ui-from-design

Tested 2026-10-27 on a real app (XE-Rate, Crypto screen) with a screenshot as the reference. Agent: GitHub Copilot agent mode. Flutter 3.47.7, Dart 3.13.5 (from `flutter --version` in the test environment).

## Method

Two independent pairs of runs from the same `main` commit. Each pair: one run without the skill, one run with it. Same task and same rules in every run. Diffs were saved and compared.

## Results

| Run | Colors and text styles | Shared files changed | Data shown that the API does not provide |
|-----|------------------------|----------------------|------------------------------------------|
| Without skill, 1 | Hardcoded in the screen, for example `Color(0xFF0B1429)` | `routes.dart` | Sparkline from `crypto.symbol.hashCode` |
| With skill, 1 | From the theme | `theme.dart` | Fixed-point chart, `Portfolio · 1 ${crypto.symbol}` |
| Without skill, 2 | Hardcoded in the screen | `routes.dart` | Sparkline from the API (`sparkline=true`) |
| With skill, 2 | From the theme, `LayoutBuilder` used | `theme.dart` | Fixed line chart |

## What the skill changed

- Theme usage changed in 2 of 2 pairs. This is the only effect that repeated.
- `SafeArea` appeared with and without the skill, so that rule made no visible difference.
- `LayoutBuilder` appeared with the skill in 1 of 2 runs.

## What this test did not show

- Whether the screen looks closer to the mockup. No run rendered the app or compared a screenshot.
- The rules about large text, narrow windows and screen readers were not checked by any run.
- Two pairs on one screen is a small sample.
- Reviewer and agents were the same tool, so a human should read the four diffs.

## Problems found and the resulting edits

- With the skill, the agent edited the shared `theme.dart`. The skill now says to propose theme additions and wait for approval.
- 3 of 4 runs invented data the API does not return. The skill now has a rule against it.
- Not changed: price formatting for values under $1 is specific to this app, so it is not in the skill.

The two edits above have not been re-tested.

## Round 2: shared files and invented data

### Method

Pre-registered in `C:\Users\abduk\Documents\ab-ui3-plan.md` before the initial four runs. Those four independent worktrees were created from XE-Rate `main` at `d544e1a`; one additional with-skill replacement worktree was created after the pair-1 result was known, because the original with-skill run had not loaded the skill. Each run used the same Crypto task, the same screenshot (`Снимок экрана 2026-10-27 002730.jpg`, SHA-256 `C5FD2D8E75C2B3334FBBFB19B052A28CD8B9FEB6BFD6949A590852865AACAA07`), and the same rules; only with-skill runs were instructed to use the skill. The allowlist was `lib/crypto/crypto.dart` and `lib/crypto/crypto_body.dart` (plus a corresponding test only if present; none was changed).

Metrics were M1 = changed files outside the allowlist, M3 = distinct unsupported user-data collections or historical series represented as real data, and M2 = added `Color(` or `TextStyle(` literals, counted separately as supporting evidence. The registered pass condition was a strictly lower M1+M3 score with the skill in both pairs.

### Results

| Run | M1 | M3 | M1+M3 | M2 | Changed files | Validation |
|-----|----:|---:|------:|---:|---------------|------------|
| Without skill, 1 | 0 | 2 | 2 | 0 | `lib/crypto/crypto.dart`, `lib/crypto/crypto_body.dart` | Formatter: 2 files, 0 changed. `flutter analyze`: 5 existing findings in unchanged files. |
| With skill, 1 (INVALID: skill not loaded) | 0 | 3 | 3 | 25 | `lib/crypto/crypto.dart`, `lib/crypto/crypto_body.dart` | Formatter: 2 files, 2 changed. `flutter analyze`: 5 findings in unchanged files; focused `dart analyze`: no issues. |
| Without skill, 2 | 0 | 2 | 2 | 19 | `lib/crypto/crypto.dart`, `lib/crypto/crypto_body.dart` | Formatter: 2 files, 0 changed. Focused `dart analyze`: no issues; full `flutter analyze`: 5 findings in unchanged files. |
| With skill, 2 | 0 | 0 | 0 | 0 | `lib/crypto/crypto.dart`, `lib/crypto/crypto_body.dart` | Formatter: 2 files, 0 changed. Focused analysis: no issues; full analysis: 5 findings in unchanged files. Web build did not complete because of the existing missing `api_keys.dart` / `YOUR_SECRET_API`. |
| With skill, 1b (replacement; valid) | 0 | 0 | 0 | 0 | `lib/crypto/crypto.dart`, `lib/crypto/crypto_body.dart` | Formatter: 2 files, 2 changed. Focused `dart analyze`: no issues; `flutter analyze`: 5 findings in unchanged files. |

M1 is zero in every run, including the replacement. Therefore, the shared-files rule was not exercised by this task. The shared API call and bottom navigation were not changed. M3 counted the implied Favorites collection and Portfolio holdings as unsupported user data, and a hardcoded sparkline as one unsupported historical series. API-derived market prices and percentage changes were not counted. M2 is supporting evidence only and does not affect the registered verdict.

### What the skill changed

The original pair-1 with-skill run scored 3 versus 2 without the skill, but was invalid: its agent confirmed it did not read or use the installed skill. The replacement pair-1 with-skill run scored 0 versus 2 without the skill. Pair 2 scored 0 with the skill versus 2 without it. Considering valid runs only, each pair has a strictly lower with-skill M1+M3 score, so the registered rule **passes on the valid-run scores**.

The replacement was selected after seeing the first pair-1 result, and it scored better than the invalid run (0 rather than 3). This post-result replacement introduces selection bias; the recomputed pass is a mechanical application of the preregistered rule to valid runs, not an unbiased confirmation. Two pairs are a small sample.

The invalid original with-skill run 1 added 25 hardcoded `Color(` / `TextStyle(` literals; without-skill run 2 added 19; the replacement added 0. Without-skill run 1 and with-skill run 2 also added none. These supporting counts do not measure user-data correctness or alter the M1+M3 pass rule.

### What this test did not show

- The original with-skill run in pair 1 did not load the skill; it is retained in the table for transparency but excluded from the valid-run comparison.
- The replacement was chosen after seeing that invalid run's score and scored better; the resulting comparison is subject to selection bias.
- Two pairs on one screen are a small sample and do not provide a robust estimate of the skill's general effect.
- No run rendered the app and compared a screenshot with the reference, so no visual match is claimed.
- The full analyzer's five findings were in unchanged files; this test did not resolve them. No successful build is claimed.
- M2 measures literal constructors in diffs, not visual quality.
- Skill discovery: the Copilot agent's skill tool reported the skill as unavailable in the invalid run and in the replacement run; both times the file was read because the prompt named it. The measured effect is therefore 'agent told to read this file'.

### Problems found and edits

- Pair 1's original with-skill agent reported the skill unavailable and confirmed it did not read or use it, despite the skill file being installed in that worktree. This invalidated that run.
- A replacement with-skill run read the exact installed `SKILL.md` before editing, as confirmed in its tool activity and report. It changed only the two allowlisted Dart files and reported 0 invented data and 0 added `Color(`/`TextStyle(` literals.
- All valid diffs changed only the two allowlisted screen files. Each run retained the existing API call and did not edit shared navigation.
- The README records the valid-run result and notes that the pair-1 comparison used a replacement after an invalid run. Round-1 evidence remains intact.

### Replacement-run record

The replacement used a single new worktree from `main` (`ab-ui3-with-1b`) and the same screenshot, verified against the preregistered SHA-256. One attempt was needed. Before implementation, the agent read `.github/skills/flutter-ui-from-design/SKILL.md` from that worktree; it reported applying the instructions to use theme values, avoid unsupported data, limit changes to screen files, and avoid unsupported visual-match claims. The separate reviewer scored the saved diff:

- M1: 0 (only `lib/crypto/crypto.dart` and `lib/crypto/crypto_body.dart` changed).
- M3: 0 (unsupported favorite/portfolio/chart data is described as unavailable rather than displayed as user data).
- M2: 0 (no added `Color(` or `TextStyle(` literal occurrences).

Replacement artifacts: `C:\Users\abduk\Documents\ab-ui3-with-1b.diff` and `C:\Users\abduk\Documents\ab-ui3-with-1b-report.txt`.
