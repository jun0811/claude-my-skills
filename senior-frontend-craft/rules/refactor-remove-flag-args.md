---
title: Eliminate Boolean Flag Parameters
impact: HIGH
tags: refactoring, API design, clarity
---

## Eliminate Boolean Flag Parameters

Boolean parameters make call sites unreadable because `true`/`false` convey no meaning without reading the function signature. Replace them with an options object with named keys, or split into separate functions when the flag fundamentally changes behavior.

**Incorrect (boolean flags make call sites cryptic):**

```tsx
// What do true, false, true mean at the call site?
const ResourceTable = ({
  data,
  editable,
  showHeader,
  showPagination,
  compact,
}: {
  data: Resource[];
  editable: boolean;
  showHeader: boolean;
  showPagination: boolean;
  compact: boolean;
}) => {
  return (
    <Table
      dataSource={data}
      showHeader={showHeader}
      pagination={showPagination ? {} : false}
      size={compact ? 'small' : 'middle'}
      columns={editable ? editableColumns : readonlyColumns}
    />
  );
};

// Call site is unreadable
<ResourceTable data={instances} editable={true} showHeader={false} showPagination={true} compact={false} />

// Function with boolean flag that changes behavior entirely
const fetchResources = (type: string, useCache: boolean, includeDeleted: boolean) => {
  // ...
};

fetchResources('volumes', true, false); // what is true? what is false?
```

**Correct (named options or separate functions):**

```tsx
interface ResourceTableOptions {
  editable?: boolean;
  showHeader?: boolean;
  showPagination?: boolean;
  compact?: boolean;
}

interface ResourceTableProps {
  data: Resource[];
  options?: ResourceTableOptions;
}

const ResourceTable = ({ data, options = {} }: ResourceTableProps) => {
  const { editable = false, showHeader = true, showPagination = true, compact = false } = options;

  return (
    <Table
      dataSource={data}
      showHeader={showHeader}
      pagination={showPagination ? {} : false}
      size={compact ? 'small' : 'middle'}
      columns={editable ? editableColumns : readonlyColumns}
    />
  );
};

// Call site: every option is self-documenting
<ResourceTable data={instances} options={{ editable: true, showHeader: false }} />

// Split into separate functions when the flag changes core behavior
interface FetchResourcesParams {
  type: string;
  includeDeleted?: boolean;
}

const fetchResources = ({ type, includeDeleted = false }: FetchResourcesParams) => {
  // standard fetch logic
};

const fetchCachedResources = ({ type, includeDeleted = false }: FetchResourcesParams) => {
  // cache-first fetch logic
};

// Call sites are clear about intent
fetchCachedResources({ type: 'volumes' });
fetchResources({ type: 'volumes', includeDeleted: true });
```
