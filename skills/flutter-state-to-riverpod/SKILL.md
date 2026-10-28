---
name: flutter-state-to-riverpod
description: Use when migrating a Flutter app from setState, Provider or ChangeNotifier to Riverpod, or when writing providers, Notifiers and AsyncNotifiers. Triggers on "migrate to Riverpod", "AsyncNotifier", "ProviderScope", "ConsumerWidget", "ref.watch".
---

# Migrate Flutter state to Riverpod

Move an app to Riverpod one screen at a time, without a big-bang rewrite. Targets `flutter_riverpod` 2.x and 3.x with the `Notifier` / `AsyncNotifier` API. Check `pubspec.yaml` for the installed version first; in 3.x the old `StateProvider`, `StateNotifierProvider` and `ChangeNotifierProvider` live in `package:flutter_riverpod/legacy.dart`, so do not write new code with them.

## Before you start

1. Read `pubspec.yaml` and find the current state approach (`provider`, `setState`, `get_it`, `ChangeNotifier`).
2. List the screens and which state each one reads and writes.
3. Decide the order: start with a leaf screen that has little shared state. Do not start with the app root.
4. Not everything moves. Purely local, short-lived UI state (a `TextEditingController`, an `AnimationController`, "is the dropdown open") stays in `StatefulWidget`. Move state that is shared, async, or needs tests.

## Steps

1. **Confirm dependency scope** with the task owner before adding or changing `flutter_riverpod`. If it is already installed, preserve the existing version and wrap the app:

```dart
void main() {
  runApp(const ProviderScope(child: MyApp()));
}
```

2. **Convert one model class to a `Notifier`.** `build()` returns the initial state; methods mutate `state`.

Before (`ChangeNotifier`):

```dart
class CounterModel extends ChangeNotifier {
  int count = 0;
  void increment() {
    count++;
    notifyListeners();
  }
}
```

After:

```dart
class CounterNotifier extends Notifier<int> {
  @override
  int build() => 0;

  void increment() => state++;
}

final counterProvider =
    NotifierProvider<CounterNotifier, int>(CounterNotifier.new);
```

State must be immutable. Assign a new value (`state = [...state, item]`), do not mutate a list in place, or listeners will not fire.

3. **Async data goes into `AsyncNotifier`.** Do not hand-roll `isLoading`, `error`, `data` fields.

```dart
class TodosNotifier extends AsyncNotifier<List<Todo>> {
  @override
  Future<List<Todo>> build() => ref.watch(todoRepositoryProvider).fetchAll();

  Future<void> add(Todo todo) async {
    final repo = ref.read(todoRepositoryProvider);
    state = await AsyncValue.guard(() async {
      await repo.add(todo);
      return repo.fetchAll();
    });
  }
}

final todosProvider =
    AsyncNotifierProvider<TodosNotifier, List<Todo>>(TodosNotifier.new);
```

4. **Parameters use `family`.** For read-only data, `FutureProvider.family<Todo, String>((ref, id) => ...)` works the same in 2.x and 3.x. For a notifier that needs a parameter, the syntax differs by version: 2.x uses `FamilyNotifier` / `FamilyAsyncNotifier` with `build(arg)`, 3.x passes the argument through the notifier's constructor. Check the installed version's docs before writing it.

5. **Convert the widget.** `StatelessWidget` becomes `ConsumerWidget`; `StatefulWidget` becomes `ConsumerStatefulWidget` (the `ref` is available inside `State`).

```dart
class TodoPage extends ConsumerWidget {
  const TodoPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final todos = ref.watch(todosProvider);
    return todos.when(
      data: (items) => TodoList(items: items),
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (e, st) => ErrorView(message: '$e'),
    );
  }
}
```

6. **Replace `context.read<T>()` and `context.watch<T>()`** with `ref.read(provider.notifier)` and `ref.watch(provider)` using the rules below.

7. **Run the app and tests after each screen.** Delete the old `ChangeNotifier` and `ChangeNotifierProvider` only when nothing reads them. Remove the `provider` package last.

## The three `ref` rules

| Where | Use | Why |
|-------|-----|-----|
| Inside `build()` | `ref.watch` | rebuilds when the value changes |
| Inside callbacks (`onPressed`, `initState`) | `ref.read` | reads once, no subscription |
| Side effects (snackbar, navigation) | `ref.listen` | reacts to a change without rebuilding |

Never `ref.read` inside `build()` for values the UI shows, and never `ref.watch` inside a callback.

## Reducing rebuilds

Watch only the part you need:

```dart
final name = ref.watch(userProvider.select((u) => u.name));
```

## Providers that depend on other providers

Use `ref.watch` inside a provider's `build()` so it recomputes when the dependency changes. Do not store `ref` in a field, and do not read a `BuildContext` in a provider.

## Lifetime

Providers created with the manual syntax stay alive for the whole app unless you use `.autoDispose` (2.x) or the generator's default. If a screen's state must reset when the user leaves, use auto-dispose. If it must survive, keep it alive deliberately. Check the version's docs; defaults changed between 2.x and 3.x.

## Testing

Override dependencies with a `ProviderContainer`:

```dart
final container = ProviderContainer(overrides: [
  todoRepositoryProvider.overrideWithValue(FakeTodoRepository()),
]);
addTearDown(container.dispose);

await container.read(todosProvider.future);
expect(container.read(todosProvider).value, isNotEmpty);
```

For widget tests wrap the widget in `ProviderScope(overrides: [...], child: ...)`.

## Common mistakes

- Mixing styles: half of a screen on `Provider`, half on Riverpod. Finish one screen before the next.
- Mutating state in place (`state.add(x)`) instead of assigning a new object.
- Calling `ref.read` in `build()` and wondering why the UI never updates.
- Creating a provider inside a widget's `build()`. Providers are top-level (or generated), never created per build.
- Putting `BuildContext`, controllers or navigation inside a notifier.
- Moving ephemeral UI state into Riverpod just because it exists.
- Using `StateProvider` for anything with logic. If it has more than one method, make it a `Notifier`.
- Forgetting `ProviderScope` at the root: you get "No ProviderScope found".

## Done when

- No imports of the old state package remain in the migrated feature or screen.
- Old providers are removed only after a repository-wide search confirms they are unused.
- Remove the old package only after the final migration, not during an incremental step.
- `flutter analyze` is clean.
- Each migrated screen has at least one test with overridden providers.
