---
title: Respect Layer Boundaries
impact: CRITICAL
tags: architecture, layers, API
---

## Respect Layer Boundaries

Follow the API module -> Custom Hook -> Component flow strictly. Components never call API functions or use fetch/axios directly. This keeps networking concerns isolated, enables consistent error handling, and makes components testable without mocking HTTP.

**Incorrect (component calls API directly inside useEffect):**

```tsx
const VolumeList = () => {
  const [volumes, setVolumes] = useState<Volume[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    // Direct API call in the component — violates layer boundary
    axios
      .get('/ixcloud-api/volumes', {
        headers: { 'X-Auth-Token': localStorage.getItem('token') },
      })
      .then((res) => {
        setVolumes(res.data.volumes);
      })
      .catch((err) => {
        message.error(err.response?.data?.message ?? 'Failed to load');
      })
      .finally(() => setLoading(false));
  }, []);

  const handleDelete = async (id: string) => {
    await axios.delete(`/ixcloud-api/volumes/${id}`);
    setVolumes((prev) => prev.filter((v) => v.id !== id));
  };

  return <Table dataSource={volumes} loading={loading} /* ... */ />;
};
```

**Correct (API module -> hook -> component, each layer has one job):**

```tsx
// api/ixcloud/Volume/index.ts — API layer: HTTP only
export const volumeApi = {
  getList: () => axiosInstance.get<VolumeListResponse>('/volumes'),
  remove: (id: string) => axiosInstance.delete(`/volumes/${id}`),
};

// containers/Volumes/useVolumes.ts — Hook layer: state + orchestration
interface UseVolumesReturn {
  volumes: Volume[];
  loading: boolean;
  onDelete: (id: string) => Promise<void>;
}

export const useVolumes = (): UseVolumesReturn => {
  const [volumes, setVolumes] = useState<Volume[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    volumeApi
      .getList()
      .then((res) => setVolumes(res.data.volumes))
      .catch(() => message.error('Failed to load volumes'))
      .finally(() => setLoading(false));
  }, []);

  const onDelete = async (id: string) => {
    await volumeApi.remove(id);
    setVolumes((prev) => prev.filter((v) => v.id !== id));
  };

  return { volumes, loading, onDelete };
};

// containers/Volumes/VolumePresenter.tsx — UI layer: props only
interface VolumePresenterProps {
  volumes: Volume[];
  loading: boolean;
  onDelete: (id: string) => Promise<void>;
}

const VolumePresenter = ({ volumes, loading, onDelete }: VolumePresenterProps) => (
  <Table dataSource={volumes} loading={loading} /* ... */ />
);
```
