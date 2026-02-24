---
title: Don't Abstract Before Three Repetitions
impact: HIGH
tags: abstraction, YAGNI, premature
---

## Don't Abstract Before Three Repetitions

Wait until you see the same pattern 3 times before creating an abstraction. Premature abstraction is worse than duplication because it couples unrelated consumers to a shared interface that may evolve in conflicting directions.

**Incorrect (abstracting after seeing the pattern once):**

```tsx
// After building ONE list page, immediately creating a "generic" hook
function useResourceList<T>(endpoint: string, params?: Record<string, unknown>) {
  const [data, setData] = useState<T[]>([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({ page: 1, pageSize: 20 });
  const [filters, setFilters] = useState<Record<string, unknown>>({});
  const [sorter, setSorter] = useState<{ field: string; order: string } | null>(null);

  // 200 lines of "generic" logic that only serves one consumer
  // Every new consumer needs special cases and escape hatches
  useEffect(() => {
    setLoading(true);
    api.get<T[]>(endpoint, { ...params, ...pagination, ...filters, ...sorter })
      .then(res => setData(res.data))
      .finally(() => setLoading(false));
  }, [endpoint, params, pagination, filters, sorter]);

  return { data, loading, pagination, setPagination, filters, setFilters, sorter, setSorter };
}
```

**Correct (write the pattern inline, extract only after the third repetition):**

```tsx
// First time: Instances list — just write it directly
function useInstances() {
  const [instances, setInstances] = useState<Instance[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchInstances = useCallback(async (params: InstanceParams) => {
    setLoading(true);
    const res = await instanceApi.list(params);
    setInstances(res.data);
    setLoading(false);
  }, []);

  return { instances, loading, fetchInstances };
}

// Second time: Volumes list — similar, but notice differences
function useVolumes() {
  const [volumes, setVolumes] = useState<Volume[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchVolumes = useCallback(async (params: VolumeParams) => {
    setLoading(true);
    const res = await volumeApi.list(params);
    setVolumes(res.data.volumes); // different response shape
    setLoading(false);
  }, []);

  return { volumes, loading, fetchVolumes };
}

// Third time: NOW you see the real pattern and can extract with confidence
// because you understand the actual variations (response shapes, param types)
function useResourceList<T>(fetchFn: (params: any) => Promise<T[]>) {
  const [data, setData] = useState<T[]>([]);
  const [loading, setLoading] = useState(false);

  const fetch = useCallback(async (params: unknown) => {
    setLoading(true);
    const result = await fetchFn(params);
    setData(result);
    setLoading(false);
  }, [fetchFn]);

  return { data, loading, fetch };
}
```
