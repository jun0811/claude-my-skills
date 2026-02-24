---
title: Dependencies Flow Inward
impact: CRITICAL
tags: architecture, dependencies, coupling
---

## Dependencies Flow Inward

Inner layers (utils, types, constants) must never import from outer layers (containers, pages). Dependencies flow inward: Pages/Containers -> Hooks -> Utils/Types. Violating this creates circular dependencies and makes lower-level modules impossible to reuse.

**Incorrect (utility imports from a container, creating circular dependency):**

```tsx
// src/utils/formatResource.ts — utility importing from container layer
import { ResourceContext } from '@/containers/Resources/ResourceContext';
import { useResourceConfig } from '@/containers/Resources/useResourceConfig';

export const formatResourceName = (resource: Resource) => {
  // This utility now depends on the container layer
  const config = useResourceConfig(); // hooks can't be called in utilities!
  return `${config.prefix}-${resource.name}`;
};

// src/hooks/useResourceList.ts — hook importing from container
import { ResourceTable } from '@/containers/Resources/ResourceTable';

export const useResourceList = () => {
  // Hook depends on a UI component — wrong direction
  const columns = ResourceTable.defaultColumns;
  // ...
};
```

**Correct (dependencies flow inward, lower layers are independent):**

```tsx
// src/utils/formatResource.ts — pure utility, no outer-layer imports
export const formatResourceName = (prefix: string, resource: Resource) => {
  return `${prefix}-${resource.name}`;
};

// src/hooks/useResourceList.ts — hook imports from utils/types only
import { formatResourceName } from '@/utils/formatResource';
import type { Resource } from '@/types/resource';

export const useResourceList = (prefix: string) => {
  const [resources, setResources] = useState<Resource[]>([]);

  const formattedResources = useMemo(
    () => resources.map((r) => ({ ...r, displayName: formatResourceName(prefix, r) })),
    [resources, prefix],
  );

  return { resources: formattedResources };
};

// src/containers/Resources/ResourceContainer.tsx — container imports from hooks/utils
import { useResourceList } from '@/hooks/useResourceList';
import { formatResourceName } from '@/utils/formatResource';

const ResourceContainer = () => {
  const { resources } = useResourceList('vpc');
  return <ResourcePresenter resources={resources} />;
};
```
