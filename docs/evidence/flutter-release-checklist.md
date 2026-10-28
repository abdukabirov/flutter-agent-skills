# Evidence: flutter-release-checklist

Status: removed. Fact-check corrected several claims, but the A/B test showed identical findings with and without the skill.

Tested 2026-10-27 on XE-Rate at app `main` commit `d544e1a`. Four separate agents ran the same Android release task in independent worktrees. Flutter 3.47.7, Dart 3.13.5.

## Method

Before any run, the app's Android release configuration was inspected in `main` and recorded in `C:\Users\abduk\Documents\ab-rc-ground-truth.md`. The ground truth identified a debug release signer, a template `com.example.x_rate` application ID, a placeholder Android label, and an ignored local API-key file absent from clean worktrees. The main manifest already had `INTERNET`; signing files were already covered by `android/.gitignore`; version values were derived from `pubspec.yaml`.

Two independent pairs used the same task and rules. The "with" worktrees alone received the edited skill. Each run's findings, analyzer output, and diff were saved separately. A reviewer compared findings and diffs to the ground truth. No credentials or keystores were created, no API-key contents were accessed, and the app's `main` was not changed.

## Results

| Run | Ground-truth problems reported | Problems missed | Main changes | Validation |
|-----|-------------------------------|-----------------|--------------|------------|
| Without skill, 1 | a, c, f, h | g | Replaced debug signing, changed label to `XE-Rate`, upgraded Android build tools. c and h unresolved. | `flutter analyze`: exit 1, 5 diagnostics. No bundle build recorded. |
| With skill, 1 | a, c, f, h | g | Replaced debug signing and upgraded Android build tools. Left label, c, and h unresolved. | `flutter analyze`: exit 1, 5 diagnostics; `flutter test`: exit 1 (`test/` missing); bundle build failed before Dart compilation on Gradle/Java compatibility, then on the missing API-key import after toolchain updates. |
| Without skill, 2 | a, c, h | f, g | Replaced debug signing, changed label to `XE-Rate`, upgraded Android build tools, added unrequested README release instructions. c and h unresolved. | `flutter analyze`: exit 1, 5 diagnostics; bundle build exit 1 on missing API-key import. |
| With skill, 2 | a, c, h | f, g | Replaced debug signing, added a redundant root ignore rule, pinned `targetSdkVersion` to 36, upgraded Android build tools. c and h unresolved. | `flutter analyze`: exit 1, 5 diagnostics; `flutter test`: exit 1 (`test/` missing); bundle build exit 1 on missing API-key import. |

No run produced a Play-ready AAB. Across all four runs, analyzer reported two naming infos, the missing ignored API-key import and undefined identifier, and an `avoid_print` info. No run changed the application ID or version, and no run exposed or created signing/API-key material.

## What the skill changed

- Both with-skill runs attempted `flutter test`; the project has no `test/` directory, so both commands failed. The without-skill runs did not report this check.
- Every run moved release signing away from the debug key, so the skill did not produce a repeatable advantage on that fix.
- The two with-skill runs did not consistently identify the Android label or the existing ignored API-key file as problems. The second with-skill run added a hardcoded target SDK and redundant ignore rules. The two pairs differ in other changes too; these results do not isolate a causal skill benefit.
- The test supports retaining explicit no-secret handling and requiring evidence before changing owner-controlled settings, but does not show that the skill consistently improved release readiness.

## What this test did not show

- No run generated or signed an AAB; signing with real owner-provided material was not tested.
- The app ID and version were not validated against a Play Console listing or upload history.
- No iOS build, store submission, privacy declaration, obfuscation, staged rollout, or visual test was performed.
- Two pairs are a small sample. Agents made different choices, and several Android toolchain changes were not applied consistently.
- `flutter analyze` and all attempted app-bundle builds failed. `flutter test` failed because the project has no test directory.

## Problems found and edits

- All four runs correctly found that `android/app/build.gradle` assigned the debug signer to the release build. All moved away from that assignment; none tested a valid signed release.
- The application ID and missing API-key source remained unresolved, appropriately requiring owner input or an API key. The ignored local key value is not included in this report.
- Run 2 without the skill added README instructions not needed to fix the ground-truth issues. They give the bundle path as `build/app/outputs/bundle/release/app-release.aab`; Flutter's Android deployment guide documents `build/app/outputs/bundle/release/app.aab`. Run 2 with the skill added redundant root ignore patterns and pinned the Flutter-managed target SDK without a ground-truth target-SDK defect.
- Verdict: **TRIM**. Keep the no-secret and evidence-based signing guidance. The skill now says to use established app metadata rather than infer a label from the package name, add ignore rules only when they are not already covered, compare Play's target API requirement to Flutter's effective `targetSdk` before overriding it, and change Android build-tool versions only after a recorded compatibility error.
