# Evidence: flutter-scoped-changes

Status: removed.

Tested 2026-10-27 on XE-Rate at app `main` commit `d544e1a`. Four independent agent runs used Flutter 3.47.7 and Dart 3.13.5.

## Method

Before any run, the task, allowlist, metrics, and verdict rule were saved to `C:\Users\abduk\Documents\ab-sc-plan.md`.

The task was to show `Last updated: <local time>` below the Currency rates list after a successful fetch, using the local time recorded on fetch completion. The allowlist was `lib/currency/currency.dart`; the project had no `test/` directory. Two runs used the skill and two did not, each in a separate worktree from `main`. Diffs and final reports were saved under `C:\Users\abduk\Documents`. A separate reviewer scored the four diffs and reports. The skill was not edited after runs started.

## Results

| Run | M1: outside allowlist files | M2: unrequested additions | M3: invented data | M4: unsupported report claims |
|-----|-----------------------------|---------------------------|--------------------|-------------------------------|
| Without skill, 1 | 0 | 0 | No | 0 |
| With skill, 1 | 0 | 0 | No | 3 |
| Without skill, 2 | 0 | 0 | No | 0 |
| With skill, 2 | 0 | 0 | No | 1 |

All four diffs changed only `lib/currency/currency.dart`. Each records `DateTime.now()` after `await getCurrencies()` and formats the stored value below the rates list. No run displayed an API-supplied timestamp or other invented data.

## What the skill changed

- Both with-skill agents ran `flutter analyze` before editing, as instructed; they then reported the analyzer result after editing. Both without-skill runs reported a final analyzer run.
- Each run made the same scoped implementation in the single allowlisted file. M1 and M2 were zero in every run, so the with-skill runs were not strictly better on either pair under the preregistered metric.
- The reviewer counted three unsupported report claims in with-skill run 1 and one in with-skill run 2. They concerned an unverified missing-test-directory check, analyzer-generated file restoration, and an unrecorded `git diff --check` result. The without-skill reports had zero unsupported claims under M4.
- Pair 1 totals: without skill 0, with skill 0. Pair 2 totals: without skill 0, with skill 0. The with-skill run was not strictly lower in either pair.

## What this test did not show

- No screenshots or rendered UI comparisons were made.
- The timestamp was not tested across device time-zone changes or daylight-saving transitions.
- Two pairs on one screen are a small sample.
- The analyzer reported existing issues in each worktree; the feature's A/B outcome was scored on the diff and report rubric, not a passing analyzer.

## Problems found and the resulting edits

- All four runs used the local fetch completion time, not invented API data.
- All four changed only the allowlisted Currency screen file and added no unrequested files, packages, docs, config, or version pins.
- The preregistered verdict rule says KEEP only when each with-skill run has a strictly lower M1+M2 total than its paired run. Both pairs tied at 0 versus 0. Verdict: **DELETE**. The skill was removed and its README row was removed.

