---
title: Combine Multiple Iterations into One
impact: HIGH
tags: refactoring, performance, iteration
---

## Combine Multiple Iterations into One

When chaining `.filter().map()` or running multiple `.forEach()` passes over the same array, combine them into a single `.reduce()` or loop. This avoids creating intermediate arrays and iterating the data multiple times. For simple cases with small arrays, chaining is perfectly fine for readability -- apply this rule when arrays are large or iterations are 3+.

**Incorrect (multiple passes creating intermediate arrays):**

```tsx
const processInstances = (instances: Instance[]) => {
  // Pass 1: filter active
  const activeInstances = instances.filter((i) => i.status === 'ACTIVE');
  // Pass 2: map to view model
  const viewModels = activeInstances.map((i) => ({
    id: i.id,
    name: i.name,
    ip: i.addresses[0]?.addr,
  }));
  // Pass 3: sort
  const sorted = viewModels.sort((a, b) => a.name.localeCompare(b.name));
  return sorted;
};

// Worse: multiple forEach building separate results from same data
const categorize = (resources: Resource[]) => {
  const active: Resource[] = [];
  const errored: Resource[] = [];
  const counts = { active: 0, error: 0, other: 0 };

  resources.forEach((r) => {
    if (r.status === 'ACTIVE') active.push(r);
  });
  resources.forEach((r) => {
    if (r.status === 'ERROR') errored.push(r);
  });
  resources.forEach((r) => {
    if (r.status === 'ACTIVE') counts.active++;
    else if (r.status === 'ERROR') counts.error++;
    else counts.other++;
  });

  return { active, errored, counts };
};
```

**Correct (single pass through the data):**

```tsx
const processInstances = (instances: Instance[]) => {
  return instances
    .reduce<InstanceViewModel[]>((acc, instance) => {
      if (instance.status !== 'ACTIVE') return acc;
      acc.push({
        id: instance.id,
        name: instance.name,
        ip: instance.addresses[0]?.addr,
      });
      return acc;
    }, [])
    .sort((a, b) => a.name.localeCompare(b.name));
};

// Single pass categorization
interface CategorizedResources {
  active: Resource[];
  errored: Resource[];
  counts: { active: number; error: number; other: number };
}

const categorize = (resources: Resource[]): CategorizedResources => {
  const initial: CategorizedResources = {
    active: [],
    errored: [],
    counts: { active: 0, error: 0, other: 0 },
  };

  return resources.reduce((acc, resource) => {
    switch (resource.status) {
      case 'ACTIVE':
        acc.active.push(resource);
        acc.counts.active++;
        break;
      case 'ERROR':
        acc.errored.push(resource);
        acc.counts.error++;
        break;
      default:
        acc.counts.other++;
    }
    return acc;
  }, initial);
};
```

> **Note:** For simple, readable chains like `items.filter(x => x.active).map(x => x.name)` on small arrays, chaining is preferred. Apply the single-pass pattern when you have 3+ chained operations, large datasets, or when profiling shows the iterations as a bottleneck.
