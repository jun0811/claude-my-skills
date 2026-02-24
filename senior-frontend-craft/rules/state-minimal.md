---
title: Store Only Minimum Necessary State
impact: MEDIUM-HIGH
tags: state, minimal, optimization
---

## Store Only Minimum Necessary State

Only store what cannot be computed from other state or props. Every extra piece of state is a synchronization point that can drift out of sync, creating subtle bugs. Ask yourself: "Can I derive this from existing state?" If yes, don't store it.

**Incorrect (storing redundant state that must be manually kept in sync):**

```tsx
function InstanceList() {
  const [instances, setInstances] = useState<Instance[]>([]);
  const [filteredInstances, setFilteredInstances] = useState<Instance[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [totalCount, setTotalCount] = useState(0);
  const [activeCount, setActiveCount] = useState(0);
  const [errorCount, setErrorCount] = useState(0);

  useEffect(() => {
    const filtered = instances.filter(i =>
      i.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setFilteredInstances(filtered);
    setTotalCount(filtered.length);
    setActiveCount(filtered.filter(i => i.status === 'ACTIVE').length);
    setErrorCount(filtered.filter(i => i.status === 'ERROR').length);
    // Bug: if you add a new filter condition, you must update ALL of these
    // Bug: between setFilteredInstances and setTotalCount, state is inconsistent
  }, [instances, searchQuery]);

  return (
    <div>
      <Stats total={totalCount} active={activeCount} errors={errorCount} />
      <SearchInput value={searchQuery} onChange={setSearchQuery} />
      <Table dataSource={filteredInstances} />
    </div>
  );
}
```

**Correct (store minimal state, derive everything else):**

```tsx
function InstanceList() {
  // Only two pieces of TRUE state — everything else is derived
  const [instances, setInstances] = useState<Instance[]>([]);
  const [searchQuery, setSearchQuery] = useState('');

  // Derived values — always consistent, no sync bugs possible
  const filteredInstances = useMemo(
    () => instances.filter(i =>
      i.name.toLowerCase().includes(searchQuery.toLowerCase())
    ),
    [instances, searchQuery],
  );

  const totalCount = filteredInstances.length;
  const activeCount = filteredInstances.filter(i => i.status === 'ACTIVE').length;
  const errorCount = filteredInstances.filter(i => i.status === 'ERROR').length;

  return (
    <div>
      <Stats total={totalCount} active={activeCount} errors={errorCount} />
      <SearchInput value={searchQuery} onChange={setSearchQuery} />
      <Table dataSource={filteredInstances} />
    </div>
  );
}
```
