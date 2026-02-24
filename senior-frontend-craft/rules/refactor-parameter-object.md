---
title: Group Parameters into Object
impact: HIGH
tags: refactoring, parameters, interface
---

## Group Parameters into Object

When a function or component takes 3 or more parameters, group them into a single typed object. This makes call sites self-documenting, allows adding optional parameters without breaking existing callers, and enables destructuring with defaults.

**Incorrect (many positional parameters -- call sites are unreadable):**

```tsx
const createVolume = (
  name: string,
  size: number,
  type: string,
  zone: string,
  encrypted: boolean,
  snapshotId?: string,
  description?: string,
) => {
  return volumeApi.create({ name, size, type, zone, encrypted, snapshotId, description });
};

// Call site: what does true mean? what's the empty string for?
createVolume('data-vol', 100, 'ssd', 'zone-a', true, '', 'backup volume');

// Component with many props passed individually
const ResourceHeader = (
  title: string,
  count: number,
  loading: boolean,
  onRefresh: () => void,
  onCreate: () => void,
  showCreate: boolean,
  breadcrumbs: string[],
) => { /* ... */ };
```

**Correct (parameters grouped into typed object):**

```tsx
interface CreateVolumeParams {
  name: string;
  size: number;
  type: 'ssd' | 'hdd';
  zone: string;
  encrypted: boolean;
  snapshotId?: string;
  description?: string;
}

const createVolume = (params: CreateVolumeParams) => {
  return volumeApi.create(params);
};

// Call site: every field is named, self-documenting
createVolume({
  name: 'data-vol',
  size: 100,
  type: 'ssd',
  zone: 'zone-a',
  encrypted: true,
  description: 'backup volume',
});

// Component with grouped props interface
interface ResourceHeaderProps {
  title: string;
  count: number;
  loading: boolean;
  showCreate?: boolean;
  breadcrumbs?: string[];
  onRefresh: () => void;
  onCreate: () => void;
}

const ResourceHeader = ({ title, count, loading, onRefresh, onCreate, showCreate = true }: ResourceHeaderProps) => (
  <div className="resource-header">
    <h2>{title} ({count})</h2>
    <Space>
      <Button onClick={onRefresh} loading={loading}>Refresh</Button>
      {showCreate && <Button type="primary" onClick={onCreate}>Create</Button>}
    </Space>
  </div>
);
```
