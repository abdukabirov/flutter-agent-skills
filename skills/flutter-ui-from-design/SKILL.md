---
name: flutter-ui-from-design
description: Use when implementing responsive Flutter UI from a screenshot, mockup, Figma frame, or visual reference. Triggers on "build this UI", "implement this design", "match this screenshot", or "responsive Flutter UI".
---

# Flutter UI from design

## Read the reference

1. Find the screen's route or parent shell. Check its `ThemeData` and available image and font assets.
2. Compare the reference with nearby screens. Record differences in content order, alignment, spacing, typography, image crop, and controls.
3. If an asset shown in the reference is missing, report its path instead of substituting an unrelated image.
4. If the design shows data the app's model or API does not provide (a chart series, a portfolio value, a label), do not invent it with fixed numbers or values derived from other fields. Show an empty or placeholder state and report the gap.

## Use the theme, not values read off the picture

Take colors and text styles from the app theme. Hex codes and font sizes guessed from a screenshot break dark mode and theme changes.

Wrong:

```dart
Container(
  color: const Color(0xFF6750A4),
  child: const Text('Save', style: TextStyle(fontSize: 14, color: Colors.white)),
)
```

Right:

```dart
Container(
  color: Theme.of(context).colorScheme.primary,
  child: Text(
    'Save',
    style: Theme.of(context)
        .textTheme
        .bodyMedium!
        .copyWith(color: Theme.of(context).colorScheme.onPrimary),
  ),
)
```

If the design uses a color or style the theme does not have, do not hardcode it in the screen and do not edit the shared app theme on your own. Report the missing value, propose the theme addition, and wait for approval.

## Implement the layout

- Wrap content that must avoid system intrusions in `SafeArea`.
- Use `LayoutBuilder` when a local widget's layout depends on its parent's constraints. Branch on `constraints.maxWidth` for a layout breakpoint; do not use a device type as a proxy for available space.
- Do not copy the mockup's frame width or height into the code. Use constraints, not fixed coordinates, for the whole screen.

Wrong:

```dart
// copied from a 390 px wide mockup
SizedBox(width: 390, child: content)
```

Right:

```dart
LayoutBuilder(
  builder: (context, constraints) {
    final wide = constraints.maxWidth >= 600; // example breakpoint
    return wide ? const TwoColumnLayout() : const SingleColumnLayout();
  },
)
```

- In a `Row`, `Column`, or `Flex`, use `Expanded` when the child must fill remaining main-axis space. Keep it under that flex widget with only `StatelessWidget` or `StatefulWidget` ancestors in between.
- Use `Flexible` when the child may use flex space without being forced to fill it.
- Use `Padding` for insets and `Align` to position a child.

## Controls and accessibility

- Connect each enabled control to its action. Do not leave an enabled button with a no-op callback.
- Give every control a description a screen reader can announce. For an icon-only control, check whether the widget already provides one; if not, wrap it in `Semantics(label: '...')`. Verify with TalkBack or VoiceOver.
- Test at a narrow app window and with the platform's largest text setting. Fix overflow instead of clipping or shrinking text.

## Stay inside the task

- Do not edit shared files unless the task names them: router or global navigation, app root widget, theme files, `pubspec.yaml`, `android/`, `ios/`. If the design needs a change there, describe the exact change, explain why, and wait for approval.
- Change the screen's own files only. List other problems you notice at the end instead of fixing them.

## Compare and verify

1. Run the screen and compare its screenshot with the reference at a similar viewport. Correct structural and alignment differences before color and decoration.
2. Inspect for overflow, clipped text, unreachable controls, and content covered by the keyboard.
3. Run `dart format <changed Dart files>` and `flutter analyze`. If a relevant widget test exists, run `flutter test <test file>`.
4. Report a visual match only if you compared the rendered screen with the reference.

## Official references

- [Adaptive layout and window constraints](https://docs.flutter.dev/ui/adaptive-responsive/general)
- [Use themes to share colors and font styles](https://docs.flutter.dev/cookbook/design/themes)
- [Accessibility release checklist](https://docs.flutter.dev/ui/accessibility)
- [Accessibility: UI design and styling](https://docs.flutter.dev/ui/accessibility/ui-design-and-styling)
- [`SafeArea`](https://api.flutter.dev/flutter/widgets/SafeArea-class.html)
- [`LayoutBuilder`](https://api.flutter.dev/flutter/widgets/LayoutBuilder-class.html)
- [`Expanded`](https://api.flutter.dev/flutter/widgets/Expanded-class.html)
- [`Semantics`](https://api.flutter.dev/flutter/widgets/Semantics-class.html)
- [Dart formatting](https://docs.flutter.dev/tools/formatting)
