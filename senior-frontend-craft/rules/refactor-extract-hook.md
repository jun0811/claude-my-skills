---
title: Extract Logic into Custom Hooks
impact: CRITICAL
tags: refactoring, hooks, separation
---

## Extract Logic into Custom Hooks

When a component has data fetching, state management, or event handling mixed with rendering, extract all logic into a custom hook. The component's return statement should be the only substantial code left. This makes logic independently testable and reusable.

**Incorrect (30+ lines of logic interleaved before the JSX return):**

```tsx
const SnapshotList = () => {
  const [snapshots, setSnapshots] = useState<Snapshot[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedRows, setSelectedRows] = useState<string[]>([]);
  const [searchText, setSearchText] = useState('');
  const zone = useRecoilValue(zoneAtom);

  useEffect(() => {
    setLoading(true);
    snapshotApi
      .getList(zone.id)
      .then((res) => setSnapshots(res.data.snapshots))
      .finally(() => setLoading(false));
  }, [zone.id]);

  const filteredSnapshots = useMemo(
    () => snapshots.filter((s) => s.name.includes(searchText)),
    [snapshots, searchText],
  );

  const handleDelete = async () => {
    await Promise.all(selectedRows.map((id) => snapshotApi.remove(id)));
    setSnapshots((prev) => prev.filter((s) => !selectedRows.includes(s.id)));
    setSelectedRows([]);
    message.success('Deleted successfully');
  };

  const handleRefresh = () => {
    setLoading(true);
    snapshotApi
      .getList(zone.id)
      .then((res) => setSnapshots(res.data.snapshots))
      .finally(() => setLoading(false));
  };

  return (
    <div>
      <Input.Search value={searchText} onChange={(e) => setSearchText(e.target.value)} />
      <Button onClick={handleDelete} disabled={selectedRows.length === 0}>Delete</Button>
      <Button onClick={handleRefresh}>Refresh</Button>
      <Table
        dataSource={filteredSnapshots}
        loading={loading}
        rowSelection={{ selectedRowKeys: selectedRows, onChange: setSelectedRows }}
      />
    </div>
  );
};
```

**Correct (hook encapsulates all logic, component just renders):**

```tsx
// useSnapshots.ts
interface UseSnapshotsReturn {
  snapshots: Snapshot[];
  loading: boolean;
  searchText: string;
  selectedRows: string[];
  onSearch: (value: string) => void;
  onSelectRows: (keys: string[]) => void;
  onDelete: () => Promise<void>;
  onRefresh: () => void;
}

export const useSnapshots = (): UseSnapshotsReturn => {
  const [snapshots, setSnapshots] = useState<Snapshot[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedRows, setSelectedRows] = useState<string[]>([]);
  const [searchText, setSearchText] = useState('');
  const zone = useRecoilValue(zoneAtom);

  const fetchSnapshots = useCallback(() => {
    setLoading(true);
    snapshotApi
      .getList(zone.id)
      .then((res) => setSnapshots(res.data.snapshots))
      .finally(() => setLoading(false));
  }, [zone.id]);

  useEffect(() => {
    fetchSnapshots();
  }, [fetchSnapshots]);

  const filteredSnapshots = useMemo(
    () => snapshots.filter((s) => s.name.includes(searchText)),
    [snapshots, searchText],
  );

  const onDelete = async () => {
    await Promise.all(selectedRows.map((id) => snapshotApi.remove(id)));
    setSnapshots((prev) => prev.filter((s) => !selectedRows.includes(s.id)));
    setSelectedRows([]);
    message.success('Deleted successfully');
  };

  return {
    snapshots: filteredSnapshots,
    loading,
    searchText,
    selectedRows,
    onSearch: setSearchText,
    onSelectRows: setSelectedRows,
    onDelete,
    onRefresh: fetchSnapshots,
  };
};

// SnapshotPresenter.tsx — thin rendering layer
const SnapshotPresenter = (props: UseSnapshotsReturn) => {
  const { snapshots, loading, searchText, selectedRows, onSearch, onSelectRows, onDelete, onRefresh } = props;

  return (
    <div>
      <Input.Search value={searchText} onChange={(e) => onSearch(e.target.value)} />
      <Button onClick={onDelete} disabled={selectedRows.length === 0}>Delete</Button>
      <Button onClick={onRefresh}>Refresh</Button>
      <Table
        dataSource={snapshots}
        loading={loading}
        rowSelection={{ selectedRowKeys: selectedRows, onChange: onSelectRows }}
      />
    </div>
  );
};
```
