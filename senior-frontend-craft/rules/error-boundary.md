---
title: Isolate Failures with Error Boundaries
impact: MEDIUM
tags: error, boundary, React, resilience
---

## Isolate Failures with Error Boundaries

Wrap independent UI sections in their own error boundaries so a failure in one widget does not crash the entire page. Each boundary can show a localized fallback while the rest of the application continues to function normally.

**Incorrect (single boundary wraps the entire app — one broken widget takes down everything):**

```tsx
function App() {
  return (
    <ErrorBoundary fallback={<CrashPage />}>
      <Header />
      <Dashboard />
      <ActivityFeed />
      <Sidebar />
    </ErrorBoundary>
  );
}

// If ActivityFeed throws, the user sees CrashPage — Header, Dashboard, Sidebar all gone.
```

**Correct (each independent section has its own boundary — failures are contained):**

```tsx
function App() {
  return (
    <>
      <Header />
      <ErrorBoundary fallback={<DashboardError />}>
        <Dashboard />
      </ErrorBoundary>
      <ErrorBoundary fallback={<FeedError />}>
        <ActivityFeed />
      </ErrorBoundary>
      <ErrorBoundary fallback={<SidebarError />}>
        <Sidebar />
      </ErrorBoundary>
    </>
  );
}

// If ActivityFeed throws, only that section shows FeedError.
// Header, Dashboard, and Sidebar continue working.
```
