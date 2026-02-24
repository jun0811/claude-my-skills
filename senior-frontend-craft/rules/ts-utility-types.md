---
title: Use Built-in Utility Types Effectively
impact: MEDIUM
tags: typescript, utility-types, DRY
---

## Use Built-in Utility Types Effectively

TypeScript provides utility types (`Pick`, `Omit`, `Partial`, `Required`, `Record`, `ReturnType`, `Extract`) to derive new types from existing ones. This keeps types in sync with their source and eliminates manual duplication that drifts over time.

**Incorrect (manually redefining subsets, drifts when source type changes):**

```tsx
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
  createdAt: Date;
  updatedAt: Date;
}

// Bad: duplicated fields that will drift when User changes
interface CreateUserInput {
  name: string;
  email: string;
  role: 'admin' | 'user';
}

// Bad: duplicated fields for update
interface UpdateUserInput {
  name?: string;
  email?: string;
  role?: 'admin' | 'user';
}

// Bad: manually typing a record shape
interface UserLookup {
  [id: string]: User;
}
```

**Correct (derived types stay in sync with the source automatically):**

```tsx
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
  createdAt: Date;
  updatedAt: Date;
}

// Pick only the fields needed for creation
type CreateUserInput = Pick<User, 'name' | 'email' | 'role'>;

// Omit auto-generated fields, make the rest optional for patching
type UpdateUserInput = Partial<Omit<User, 'id' | 'createdAt' | 'updatedAt'>>;

// Type-safe dictionary
type UserLookup = Record<string, User>;

// Extract return type from an existing function
type FetchResult = Awaited<ReturnType<typeof fetchUser>>;

// Derive props from a component
type ButtonVariant = React.ComponentProps<typeof Button>['variant'];
```
