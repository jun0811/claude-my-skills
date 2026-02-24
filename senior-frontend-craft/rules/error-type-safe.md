---
title: Type-Safe Error Handling with Result Pattern
impact: MEDIUM
tags: error, types, Result, safety
---

## Type-Safe Error Handling with Result Pattern

Instead of try/catch where the error type is `unknown`, use a Result type that makes success and failure explicit in the type system. Callers are forced to handle both branches, eliminating forgotten error paths.

**Incorrect (try/catch with unknown error — no type safety, easy to forget handling):**

```tsx
async function fetchUser(id: string) {
  try {
    const res = await api.get(`/users/${id}`);
    return res.data;
  } catch (e) {
    // e is `unknown` — no structure, no type help
    console.error(e);
    return null; // caller might forget to check for null
  }
}

// Caller has no idea what errors are possible
const user = await fetchUser('123');
user.name; // potential runtime error if null
```

**Correct (Result type forces callers to handle both success and failure):**

```tsx
type AppError = { code: string; message: string };
type Result<T> = { ok: true; data: T } | { ok: false; error: AppError };

async function fetchUser(id: string): Promise<Result<User>> {
  try {
    const res = await api.get<User>(`/users/${id}`);
    return { ok: true, data: res.data };
  } catch (e) {
    return {
      ok: false,
      error: { code: 'FETCH_FAILED', message: `Failed to fetch user ${id}` },
    };
  }
}

// Caller must check the discriminant — TypeScript enforces it
const result = await fetchUser('123');
if (!result.ok) {
  showError(result.error.message);
  return;
}
// TypeScript narrows: result.data is User here
console.log(result.data.name);
```
