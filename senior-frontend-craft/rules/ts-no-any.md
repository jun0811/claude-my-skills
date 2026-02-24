---
title: Ban any, Use unknown with Type Guards
impact: HIGH
tags: typescript, any, type-safety
---

## Ban any, Use unknown with Type Guards

`any` silently disables all type checking and lets errors propagate deep into your codebase. Use `unknown` to accept arbitrary data safely, then narrow with type guard functions before accessing properties.

**Incorrect (any disables type checking, runtime crash goes undetected):**

```tsx
function processApiResponse(response: any) {
  // No errors at compile time, crashes at runtime if shape is wrong
  return {
    id: response.data.id,
    name: response.data.user.name,
    email: response.data.user.email,
  };
}

// Also bad: catch block with any
try {
  await fetchUser();
} catch (error: any) {
  console.log(error.message); // crashes if error is not an Error object
}
```

**Correct (unknown with type guards ensures safety at every access point):**

```tsx
interface UserResponse {
  data: {
    id: string;
    user: { name: string; email: string };
  };
}

function isUserResponse(value: unknown): value is UserResponse {
  return (
    typeof value === 'object' &&
    value !== null &&
    'data' in value &&
    typeof (value as Record<string, unknown>).data === 'object'
  );
}

function processApiResponse(response: unknown): UserResponse['data'] | null {
  if (!isUserResponse(response)) {
    console.error('Unexpected response shape', response);
    return null;
  }
  // TypeScript knows the full shape here
  return {
    id: response.data.id,
    name: response.data.user.name,
    email: response.data.user.email,
  };
}

// Safe error handling
try {
  await fetchUser();
} catch (error: unknown) {
  const message = error instanceof Error ? error.message : 'Unknown error';
  console.error(message);
}
```
