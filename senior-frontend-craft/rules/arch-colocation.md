---
title: Colocate Related Code
impact: CRITICAL
tags: architecture, organization, colocation
---

## Colocate Related Code

Keep files that change together close together. Feature-specific hooks, types, constants, and helpers belong in the feature folder, not in global directories. Move code to shared locations only when a second consumer appears.

**Incorrect (feature-specific code scattered across global directories):**

```
src/
├── utils/
│   └── formatInstanceStatus.ts    # only used by Instances feature
├── types/
│   └── instanceFilters.ts         # only used by Instances feature
├── constants/
│   └── instanceTableColumns.ts    # only used by Instances feature
├── hooks/
│   └── useInstancePolling.ts      # only used by Instances feature
└── containers/
    └── Instances/
        └── index.tsx              # imports from 4 different global dirs
```

```tsx
// containers/Instances/index.tsx
import { formatInstanceStatus } from '@/utils/formatInstanceStatus';
import { InstanceFilters } from '@/types/instanceFilters';
import { INSTANCE_COLUMNS } from '@/constants/instanceTableColumns';
import { useInstancePolling } from '@/hooks/useInstancePolling';
```

**Correct (feature-specific code lives in the feature directory):**

```
src/
├── hooks/
│   └── useZones.ts                # shared across multiple features
├── containers/
│   └── Instances/
│       ├── index.tsx
│       ├── InstanceContainer.tsx
│       ├── InstancePresenter.tsx
│       ├── useInstance.ts          # feature-specific hook
│       ├── useInstancePolling.ts   # feature-specific hook
│       ├── constants.ts            # INSTANCE_COLUMNS, STATUS_MAP
│       ├── types.ts                # InstanceFilters, InstanceRow
│       └── serializers.ts          # formatInstanceStatus
```

```tsx
// containers/Instances/InstanceContainer.tsx
import { useInstance } from './useInstance';
import { useInstancePolling } from './useInstancePolling';
import { INSTANCE_COLUMNS } from './constants';
import type { InstanceFilters } from './types';
import { useZones } from '@/hooks/useZones'; // truly shared hook
```
