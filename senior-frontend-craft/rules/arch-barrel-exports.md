---
title: Define Public API with Barrel Exports
impact: HIGH
tags: architecture, modules, exports
---

## Define Public API with Barrel Exports

Each feature folder exposes its public API through an `index.ts` barrel file. External consumers import only from the barrel, never from internal module paths. This creates a clear boundary between public and private code, making internal refactoring safe.

**Incorrect (external features import deep internal paths):**

```tsx
// src/containers/Dashboard/DashboardContainer.tsx
// Reaching into Network's internal structure — breaks if files are reorganized
import { useNetworkList } from '@/containers/NetworkGroups/Networks/hooks/useNetworkList';
import { NetworkStatusBadge } from '@/containers/NetworkGroups/Networks/components/NetworkStatusBadge';
import { formatSubnet } from '@/containers/NetworkGroups/Networks/utils/formatSubnet';
import type { NetworkRow } from '@/containers/NetworkGroups/Networks/types/NetworkRow';
```

**Correct (feature exposes public API via index.ts, consumers use barrel import):**

```tsx
// src/containers/NetworkGroups/Networks/index.ts — barrel file
// Explicitly declares what is public
export { NetworkContainer as default } from './NetworkContainer';
export { useNetworkList } from './useNetworkList';
export { NetworkStatusBadge } from './components/NetworkStatusBadge';
export type { NetworkRow } from './types';

// Internal modules NOT exported — they stay private:
// ./serializers.ts
// ./constants.ts
// ./useNetworkPolling.ts

// src/containers/Dashboard/DashboardContainer.tsx — clean imports
import NetworkContainer, {
  useNetworkList,
  NetworkStatusBadge,
  type NetworkRow,
} from '@/containers/NetworkGroups/Networks';
```
