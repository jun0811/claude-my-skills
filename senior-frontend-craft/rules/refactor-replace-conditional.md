---
title: Replace Conditionals with Map or Strategy
impact: HIGH
tags: refactoring, conditionals, maintainability
---

## Replace Conditionals with Map or Strategy

When you have switch/if-else chains that map values to outcomes, replace them with a `Record` or `Map`. This eliminates branching, makes the mapping declarative and exhaustive, and allows adding new cases without modifying control flow.

**Incorrect (switch/if-else chains that grow with each new status):**

```tsx
const getStatusConfig = (status: string) => {
  switch (status) {
    case 'ACTIVE':
      return { color: 'green', icon: <CheckCircleOutlined />, label: 'Running' };
    case 'SHUTOFF':
      return { color: 'red', icon: <StopOutlined />, label: 'Stopped' };
    case 'BUILD':
      return { color: 'blue', icon: <LoadingOutlined />, label: 'Building' };
    case 'ERROR':
      return { color: 'red', icon: <CloseCircleOutlined />, label: 'Error' };
    case 'RESIZE':
      return { color: 'orange', icon: <LoadingOutlined />, label: 'Resizing' };
    case 'REBOOT':
      return { color: 'orange', icon: <LoadingOutlined />, label: 'Rebooting' };
    default:
      return { color: 'default', icon: <QuestionOutlined />, label: status };
  }
};

// Another common case: rendering different components based on type
const renderDetail = (type: string, data: any) => {
  if (type === 'instance') return <InstanceDetail data={data} />;
  if (type === 'volume') return <VolumeDetail data={data} />;
  if (type === 'network') return <NetworkDetail data={data} />;
  return null;
};
```

**Correct (declarative Record/Map -- add new entries without changing logic):**

```tsx
interface StatusConfig {
  color: string;
  icon: React.ReactNode;
  label: string;
}

const STATUS_CONFIG: Record<string, StatusConfig> = {
  ACTIVE: { color: 'green', icon: <CheckCircleOutlined />, label: 'Running' },
  SHUTOFF: { color: 'red', icon: <StopOutlined />, label: 'Stopped' },
  BUILD: { color: 'blue', icon: <LoadingOutlined />, label: 'Building' },
  ERROR: { color: 'red', icon: <CloseCircleOutlined />, label: 'Error' },
  RESIZE: { color: 'orange', icon: <LoadingOutlined />, label: 'Resizing' },
  REBOOT: { color: 'orange', icon: <LoadingOutlined />, label: 'Rebooting' },
} as const;

const DEFAULT_STATUS: StatusConfig = { color: 'default', icon: <QuestionOutlined />, label: 'Unknown' };

const getStatusConfig = (status: string): StatusConfig => STATUS_CONFIG[status] ?? DEFAULT_STATUS;

// Component map pattern for rendering by type
const DETAIL_COMPONENTS: Record<string, React.ComponentType<{ data: any }>> = {
  instance: InstanceDetail,
  volume: VolumeDetail,
  network: NetworkDetail,
};

const renderDetail = (type: string, data: any) => {
  const Component = DETAIL_COMPONENTS[type];
  return Component ? <Component data={data} /> : null;
};
```
