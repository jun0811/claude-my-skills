---
title: Use as const for Literal Types
impact: MEDIUM
tags: typescript, const, immutability
---

## Use as const for Literal Types

`as const` narrows types to their exact literal values and makes objects deeply readonly. This is ideal for configuration objects, action types, and any value set that should be fixed at compile time, enabling TypeScript to derive union types from arrays and enforce immutability.

**Incorrect (widened types, no literal inference):**

```tsx
// Type is string[] — TypeScript forgets the actual values
const ROLES = ['admin', 'editor', 'viewer'];

// Type is { type: string; payload: string } — too wide
const action = { type: 'INCREMENT', payload: 'count' };

// Must manually define a redundant type
type Role = 'admin' | 'editor' | 'viewer';

// No compile-time check — any string is accepted
function hasRole(user: { roles: string[] }, role: string): boolean {
  return user.roles.includes(role);
}

hasRole(user, 'admni'); // typo not caught
```

**Correct (literal types preserved, union derived automatically):**

```tsx
// Type is readonly ['admin', 'editor', 'viewer']
const ROLES = ['admin', 'editor', 'viewer'] as const;

// Derived union type: 'admin' | 'editor' | 'viewer'
type Role = (typeof ROLES)[number];

// Type-safe role checking
function hasRole(user: { roles: Role[] }, role: Role): boolean {
  return user.roles.includes(role);
}

hasRole(user, 'admni'); // compile error: not assignable to type Role

// Config objects become deeply readonly with exact literal types
const API_CONFIG = {
  baseUrl: 'https://api.example.com',
  timeout: 5000,
  retries: 3,
  methods: ['GET', 'POST', 'PUT'] as const,
} as const;

// Type is 'https://api.example.com', not string
type BaseUrl = typeof API_CONFIG.baseUrl;

// Type is 'GET' | 'POST' | 'PUT', not string
type AllowedMethod = (typeof API_CONFIG.methods)[number];
```
