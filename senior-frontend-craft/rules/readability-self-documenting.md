---
title: Code Should Explain Itself
impact: MEDIUM
tags: readability, comments, self-documenting
---

## Code Should Explain Itself

Prefer clear code over comments. If you need a comment to explain WHAT code does, rename or restructure instead. Reserve comments for explaining WHY — business rules, workarounds, and non-obvious constraints.

**Incorrect (comments explain what the code does — redundant and prone to going stale):**

```tsx
function OrderSummary({ order }: { order: Order }) {
  // Check if user is premium and order is above threshold
  if (order.user.type === 'premium' && order.total > 10000) {
    // Apply 15% discount
    const d = order.total * 0.85;
    // Check if coupon is valid
    const c = order.coupon && order.coupon.expiresAt > new Date();
    // Apply additional coupon discount
    const finalPrice = c ? d - order.coupon!.amount : d;
    // Round to 2 decimal places
    const rounded = Math.round(finalPrice * 100) / 100;
    return <Price value={rounded} />;
  }

  return <Price value={order.total} />;
}
```

**Correct (code is self-documenting; comments explain WHY, not WHAT):**

```tsx
const PREMIUM_DISCOUNT_RATE = 0.15;
const PREMIUM_DISCOUNT_THRESHOLD = 10_000;

function OrderSummary({ order }: { order: Order }) {
  const isPremiumEligible = order.user.type === 'premium' && order.total > PREMIUM_DISCOUNT_THRESHOLD;

  if (!isPremiumEligible) {
    return <Price value={order.total} />;
  }

  const discountedTotal = order.total * (1 - PREMIUM_DISCOUNT_RATE);
  const isCouponValid = order.coupon && order.coupon.expiresAt > new Date();

  // Coupon stacks with premium discount per 2024 Q3 pricing policy (JIRA-4521)
  const finalPrice = isCouponValid ? discountedTotal - order.coupon!.amount : discountedTotal;

  return <Price value={roundCurrency(finalPrice)} />;
}
```
