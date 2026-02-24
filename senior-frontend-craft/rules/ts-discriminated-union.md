---
title: Use Discriminated Unions for Type-Safe Branching
impact: HIGH
tags: typescript, unions, type-safety
---

## Use Discriminated Unions for Type-Safe Branching

A shared literal type field (the discriminant) lets TypeScript automatically narrow union members in `switch` and `if` statements. This eliminates impossible states at the type level, preventing bugs where conflicting fields coexist.

**Incorrect (all fields optional, allows impossible states like `{ loading: true, error: "fail" }`):**

```tsx
type ApiResponse = {
  data?: User;
  error?: string;
  loading?: boolean;
};

function renderUser(response: ApiResponse) {
  // No narrowing — must defensively check every field
  if (response.loading) {
    return <Spinner />;
  }
  if (response.error) {
    return <ErrorBanner message={response.error} />;
  }
  // response.data could still be undefined even here
  return <UserCard name={response.data?.name ?? 'Unknown'} />;
}
```

**Correct (discriminant field `status` makes each state explicit and mutually exclusive):**

```tsx
type ApiResponse =
  | { status: 'loading' }
  | { status: 'success'; data: User }
  | { status: 'error'; error: string };

function renderUser(response: ApiResponse) {
  switch (response.status) {
    case 'loading':
      return <Spinner />;
    case 'success':
      // TypeScript knows `data` exists here
      return <UserCard name={response.data.name} />;
    case 'error':
      // TypeScript knows `error` exists here
      return <ErrorBanner message={response.error} />;
  }
}
```
