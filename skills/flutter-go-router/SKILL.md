---
name: flutter-go-router
description: Use when adding or fixing navigation in a Flutter app with go_router, including routes, path parameters, auth redirects, nested bottom navigation, and deep links. Triggers on "GoRouter", "GoRoute", "StatefulShellRoute", "auth redirect", "pathParameters".
---

# Navigation with go_router

Set up declarative routing with `go_router`. Check `pubspec.yaml` for the installed version first; this skill uses the current API (`state.pathParameters`, `state.uri`, `state.matchedLocation`). Older code used `state.params` and `state.queryParams`; those no longer exist.

## Basic setup

Create the router once, outside `build()`:

```dart
final router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomePage(),
      routes: [
        GoRoute(
          path: 'product/:id',
          builder: (context, state) =>
              ProductPage(id: state.pathParameters['id']!),
        ),
      ],
    ),
    GoRoute(path: '/login', builder: (context, state) => const LoginPage()),
  ],
);

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) =>
      MaterialApp.router(routerConfig: router);
}
```

Child routes use a path without the leading slash (`'product/:id'`); top-level routes start with `/`.

## go vs push

- `context.go('/product/42')` replaces the stack with the location. Use it for normal navigation, tabs, and deep links.
- `context.push('/product/42')` adds on top of the current stack and returns a value on `pop`. Use it for dialogs-like flows ("pick an item and return").
- `context.pop()` goes back. Do not mix `Navigator.push` and `go_router` for the same flow.

## Passing data

- IDs and filters go in the path or query: `/product/42?tab=reviews` and read with `state.pathParameters['id']` and `state.uri.queryParameters['tab']`.
- Avoid `extra` for anything the page needs to work. `extra` is lost on a web refresh and does not exist for a deep link. Load the object by ID in the page.

## Auth redirects

Redirect from one place, and rebuild when auth changes with `refreshListenable`:

```dart
final router = GoRouter(
  refreshListenable: authNotifier, // a Listenable that notifies on login/logout
  redirect: (context, state) {
    final loggedIn = authNotifier.isLoggedIn;
    final onLogin = state.matchedLocation == '/login';

    if (!loggedIn) return onLogin ? null : '/login';
    if (onLogin) return '/';
    return null; // no redirect
  },
  routes: [ /* ... */ ],
);
```

Rules that prevent redirect loops:

- Always return `null` when no redirect is needed.
- Every redirect target must itself return `null` for the same state.
- Never redirect to a location that the same function redirects away from.
- If the auth state is still loading, show a splash route, not `/login`, so users do not flash to the login page.

## Bottom navigation with state kept per tab

Use `StatefulShellRoute.indexedStack`:

```dart
StatefulShellRoute.indexedStack(
  builder: (context, state, navigationShell) =>
      ScaffoldWithNavBar(navigationShell: navigationShell),
  branches: [
    StatefulShellBranch(routes: [
      GoRoute(path: '/home', builder: (c, s) => const HomeTab()),
    ]),
    StatefulShellBranch(routes: [
      GoRoute(path: '/profile', builder: (c, s) => const ProfileTab()),
    ]),
  ],
)
```

In the nav bar:

```dart
NavigationBar(
  selectedIndex: navigationShell.currentIndex,
  onDestinationSelected: (index) => navigationShell.goBranch(
    index,
    initialLocation: index == navigationShell.currentIndex,
  ),
  destinations: const [ /* ... */ ],
)
```

`initialLocation: true` on the current tab makes tapping it again return to the tab's root.

## Deep links

1. Make every screen reachable by a path. If a page can only be reached with `extra`, it cannot be deep linked.
2. Android: add an intent filter for the scheme or host in `AndroidManifest.xml`; for https links also host `assetlinks.json` on the domain.
3. iOS: add Associated Domains (`applinks:example.com`) and host `apple-app-site-association` on the domain.
4. Test without publishing anything:

```bash
# Android
adb shell am start -a android.intent.action.VIEW -d "https://example.com/product/42"

# iOS simulator
xcrun simctl openurl booted "https://example.com/product/42"
```

5. For Flutter web, call `usePathUrlStrategy()` before `runApp` to remove the `#` from URLs, and configure the server to serve `index.html` for unknown paths.

## Errors and unknown routes

Provide `errorBuilder` so a bad link shows a real "not found" page instead of the default error screen.

## Common mistakes

- Creating `GoRouter(...)` inside `build()`. Every rebuild makes a new router and resets navigation. Make it a top-level variable, or a provider if it depends on app state.
- Redirect loops (see rules above).
- Using `extra` as the main way to pass data.
- Absolute paths for child routes (`'/product/:id'` under `'/'` registers a different route than intended).
- `context.go` when the user expects back to work: use `push` for flows with a back button.
- Forgetting `refreshListenable`, so login state changes do not trigger redirect.
- Parsing the ID without handling bad input: `int.tryParse(state.pathParameters['id'] ?? '')` and show a not-found page on null.

## Verify

- Open every top-level and parameterized route directly from a cold start.
- Try missing or malformed parameters and confirm they reach a not-found state.
- Open an unknown route and confirm `errorBuilder` renders a useful page.
- Test loading, logged-out, and logged-in auth states; confirm no redirect loop.
- For `StatefulShellRoute`, switch tabs, reselect a tab, and verify each branch preserves its expected stack.
- On web, refresh a deep link and verify the server fallback serves `index.html` when path URLs are enabled.
