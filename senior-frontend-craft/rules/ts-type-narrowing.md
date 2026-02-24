---
title: Leverage Type Narrowing over Assertions
impact: HIGH
tags: typescript, narrowing, guards
---

## Leverage Type Narrowing over Assertions

Use control flow narrowing (`typeof`, `in`, `instanceof`, discriminant checks) instead of type assertions (`as`). Assertions tell the compiler to trust you blindly; narrowing proves correctness through runtime checks that TypeScript can verify.

**Incorrect (type assertions bypass safety, crash silently when wrong):**

```tsx
interface Admin {
  role: 'admin';
  permissions: string[];
}

interface Guest {
  role: 'guest';
  visitCount: number;
}

function getLabel(user: Admin | Guest): string {
  // Dangerous: assertion doesn't verify anything at runtime
  const admin = user as Admin;
  return `Admin with ${admin.permissions.length} permissions`;
  // Crashes when user is actually a Guest
}

// Also bad: non-null assertion on potentially null values
function getElement() {
  const el = document.querySelector('.header')!; // crashes if not found
  el.classList.add('active');
}
```

**Correct (narrowing with runtime checks that TypeScript understands):**

```tsx
interface Admin {
  role: 'admin';
  permissions: string[];
}

interface Guest {
  role: 'guest';
  visitCount: number;
}

// Discriminant narrowing
function getLabel(user: Admin | Guest): string {
  if (user.role === 'admin') {
    // TypeScript narrows to Admin automatically
    return `Admin with ${user.permissions.length} permissions`;
  }
  // TypeScript narrows to Guest here
  return `Guest (${user.visitCount} visits)`;
}

// `in` operator narrowing
function describe(shape: Circle | Rectangle): string {
  if ('radius' in shape) {
    return `Circle with radius ${shape.radius}`;
  }
  return `Rectangle ${shape.width}x${shape.height}`;
}

// Null check instead of non-null assertion
function getElement() {
  const el = document.querySelector('.header');
  if (!el) {
    throw new Error('Header element not found');
  }
  // TypeScript narrows to Element (non-null) after the check
  el.classList.add('active');
}
```
