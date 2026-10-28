---
name: flutter-testing
description: Use when writing or fixing Flutter tests, including unit tests, widget tests with testWidgets, golden tests, integration_test, and mocks. Triggers on "write tests for", "flutter test", "testWidgets", "golden test", "mocktail", "pumpAndSettle timed out".
---

# Flutter testing

Write tests that fail when behavior breaks. A test that only checks "no exception was thrown" is not a test.

## Choose the level

| Level | Use for | Command |
|-------|---------|---------|
| Unit (`test`) | Pure Dart: parsers, models, repositories, notifiers | `flutter test` |
| Widget (`testWidgets`) | One screen or component: taps, text, states | `flutter test` |
| Golden | Pixel-level look of a stable component | `flutter test` |
| Integration (`integration_test`) | Whole app on a device or emulator | `flutter test integration_test` |

Most tests should be unit and widget tests. Write few integration tests, for the critical flows only (login, purchase).

## Unit test

Arrange, act, assert. One behavior per test; name it as a sentence.

```dart
void main() {
  group('CartNotifier', () {
    test('adding the same item twice increases quantity', () {
      final cart = CartNotifier();

      cart.add(const Item(id: 'a', price: 5));
      cart.add(const Item(id: 'a', price: 5));

      expect(cart.quantityOf('a'), 2);
      expect(cart.total, 10);
    });
  });
}
```

## Widget test

Wrap the widget in the app shell it needs (`MaterialApp`, theme, `ProviderScope`), then `pump`, interact, `pump` again.

```dart
testWidgets('shows error text when email is invalid', (tester) async {
  await tester.pumpWidget(const MaterialApp(home: LoginPage()));

  await tester.enterText(find.byKey(const Key('email')), 'not-an-email');
  await tester.tap(find.byKey(const Key('submit')));
  await tester.pump(); // rebuild after the tap

  expect(find.text('Enter a valid email'), findsOneWidget);
});
```

Finders to prefer: `find.byKey`, `find.text`, `find.byType`, `find.byIcon`, `find.bySemanticsLabel`. Give widgets that you need to find a `Key`; do not find by index.

### pump, pumpAndSettle

- `await tester.pump()` runs one frame. Use it after taps and `setState`.
- `await tester.pump(const Duration(seconds: 1))` advances fake time (for timers and animations).
- `await tester.pumpAndSettle()` pumps until nothing is scheduled. It times out if something animates forever (a `CircularProgressIndicator`, a repeating animation). In that case, pump a fixed duration instead.
- Never `Future.delayed` or `sleep` in a widget test to wait for UI.

### Screen size

```dart
tester.view.physicalSize = const Size(400, 800);
tester.view.devicePixelRatio = 1.0;
addTearDown(tester.view.reset);
```

## Fakes and mocks

- Depend on interfaces (abstract classes) so the test can pass a fake.
- Prefer a hand-written fake for simple dependencies. For call verification use `mocktail` (no code generation) or `mockito`.
- Tests must never hit the real network, the real clock, or real storage. Use `SharedPreferences.setMockInitialValues({})`, an in-memory database, or fakes.
- With Riverpod, override providers: `ProviderScope(overrides: [repoProvider.overrideWithValue(FakeRepo())], child: ...)`.

```dart
class MockRepo extends Mock implements TodoRepository {}

test('load emits error state when repository throws', () async {
  final repo = MockRepo();
  when(() => repo.fetchAll()).thenThrow(Exception('offline'));
  // ... build the notifier with repo, call load, expect error state
  verify(() => repo.fetchAll()).called(1);
});
```

## Golden tests

```dart
testWidgets('ProfileCard matches golden', (tester) async {
  await tester.pumpWidget(const MaterialApp(home: ProfileCard(name: 'Ada')));
  await expectLater(
    find.byType(ProfileCard),
    matchesGoldenFile('goldens/profile_card.png'),
  );
});
```

Generate or update the images with `flutter test --update-goldens`, and commit them.

- Goldens render differently on macOS, Linux and Windows. Generate and compare on the same OS (usually the CI runner), or use a package built for it such as `alchemist`.
- Only use goldens for stable, visual components. Do not golden a whole screen with live data.
- Review golden diffs by eye in the PR. Do not blindly update them.

## Integration tests

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('user can sign in', (tester) async {
    app.main();
    await tester.pumpAndSettle();
    // enterText, tap, expect
  });
}
```

Put them in `integration_test/`, add `integration_test` to `dev_dependencies` from the SDK, and run on a device or emulator.

## Common mistakes

- Asserting nothing, or asserting only `findsWidgets` when you mean an exact count.
- Forgetting `await` before `tester.tap`, `pump`, or `expectLater`.
- Missing `MaterialApp` or `Directionality` around the widget (error: "No Directionality" or "No MediaQuery").
- Testing private implementation (a widget's internal state) instead of what the user sees.
- Shared mutable state between tests. Create objects inside `setUp` or inside each test.
- Not disposing: `addTearDown(container.dispose)` for `ProviderContainer`, `controller.close()` for streams.
- Real `DateTime.now()` in logic under test. Inject a clock.
- Flaky tests that depend on timing. Pump fake time instead.

## Done when

`flutter test` passes twice in a row, a deliberately broken behavior makes the new test fail (check this once), and `flutter analyze` is clean.
