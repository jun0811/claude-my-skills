---
title: Validate Early, Fail Immediately
impact: MEDIUM
tags: error, validation, guard
---

## Validate Early, Fail Immediately

Check preconditions at the function entry point. Do not let invalid data flow deep into the system before failing — late failures produce confusing stack traces and waste computation.

**Incorrect (validation happens deep inside, after significant processing):**

```tsx
function processOrder(order: Order | null) {
  const items = order?.items ?? [];
  const subtotal = items.reduce((sum, item) => sum + item.price * item.qty, 0);
  const tax = subtotal * 0.1;
  const shipping = calculateShipping(items);
  const total = subtotal + tax + shipping;

  // Validation buried 10 lines deep — all work above was wasted
  if (!order) {
    throw new Error('Order is required');
  }
  if (items.length === 0) {
    throw new Error('Order must have at least one item');
  }

  return createInvoice(order, total);
}
```

**Correct (guard clauses at the top reject invalid input immediately):**

```tsx
function processOrder(order: Order | null) {
  if (!order) {
    throw new Error('Order is required');
  }
  if (order.items.length === 0) {
    throw new Error('Order must have at least one item');
  }

  // Main logic runs only when preconditions are met
  const subtotal = order.items.reduce((sum, item) => sum + item.price * item.qty, 0);
  const tax = subtotal * 0.1;
  const shipping = calculateShipping(order.items);
  const total = subtotal + tax + shipping;

  return createInvoice(order, total);
}
```
