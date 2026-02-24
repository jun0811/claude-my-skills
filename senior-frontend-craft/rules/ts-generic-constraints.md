---
title: Constrain Generics for Better Inference
impact: HIGH
tags: typescript, generics, constraints
---

## Constrain Generics for Better Inference

Use `extends` to constrain generic type parameters. This gives callers full autocomplete, ensures compile-time errors for invalid arguments, and lets TypeScript infer precise return types.

**Incorrect (unconstrained key parameter, no type safety on access):**

```tsx
function getProperty<T>(obj: T, key: string): unknown {
  // TypeScript cannot verify `key` exists on `obj`
  return (obj as any)[key];
}

const user = { name: 'Alice', age: 30 };
getProperty(user, 'naem'); // typo not caught, returns undefined at runtime
```

**Correct (constrained key via `keyof`, fully type-safe with inferred return type):**

```tsx
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: 'Alice', age: 30 };
getProperty(user, 'name');  // return type inferred as string
getProperty(user, 'age');   // return type inferred as number
getProperty(user, 'naem');  // compile error: '"naem"' is not assignable

// Practical example: type-safe event handler factory
function createHandler<T extends Record<string, (...args: any[]) => void>>(
  handlers: T,
) {
  return <K extends keyof T>(event: K, ...args: Parameters<T[K]>) => {
    handlers[event](...args);
  };
}

const dispatch = createHandler({
  click: (x: number, y: number) => console.log(x, y),
  submit: (formData: FormData) => console.log(formData),
});

dispatch('click', 10, 20);        // OK
dispatch('submit', new FormData()); // OK
dispatch('click', 'wrong');        // compile error
```
