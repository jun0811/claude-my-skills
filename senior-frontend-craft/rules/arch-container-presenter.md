---
title: Separate Container from Presenter
impact: CRITICAL
tags: architecture, separation, testing
---

## Separate Container from Presenter

Container components handle data fetching, state management, and business logic. Presenter components are pure UI that receive everything through props, making them trivially testable and reusable.

**Incorrect (component fetches data and renders UI in one place):**

```tsx
const UserProfile = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const { id } = useParams<{ id: string }>();

  useEffect(() => {
    setLoading(true);
    fetchUser(id)
      .then(setUser)
      .finally(() => setLoading(false));
  }, [id]);

  const handleDelete = async () => {
    await deleteUser(id);
    message.success('User deleted');
    history.push('/users');
  };

  if (loading) return <Spin />;

  return (
    <Card title={user?.name}>
      <Descriptions>
        <Descriptions.Item label="Email">{user?.email}</Descriptions.Item>
        <Descriptions.Item label="Role">{user?.role}</Descriptions.Item>
      </Descriptions>
      <Button danger onClick={handleDelete}>Delete</Button>
    </Card>
  );
};
```

**Correct (hook extracts logic, presenter receives props only):**

```tsx
// useUserProfile.ts
interface UseUserProfileReturn {
  user: User | null;
  loading: boolean;
  onDelete: () => Promise<void>;
}

const useUserProfile = (id: string): UseUserProfileReturn => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const history = useHistory();

  useEffect(() => {
    setLoading(true);
    fetchUser(id)
      .then(setUser)
      .finally(() => setLoading(false));
  }, [id]);

  const onDelete = async () => {
    await deleteUser(id);
    message.success('User deleted');
    history.push('/users');
  };

  return { user, loading, onDelete };
};

// UserProfilePresenter.tsx — pure UI, props only
interface UserProfilePresenterProps {
  user: User | null;
  loading: boolean;
  onDelete: () => void;
}

const UserProfilePresenter = ({ user, loading, onDelete }: UserProfilePresenterProps) => {
  if (loading) return <Spin />;

  return (
    <Card title={user?.name}>
      <Descriptions>
        <Descriptions.Item label="Email">{user?.email}</Descriptions.Item>
        <Descriptions.Item label="Role">{user?.role}</Descriptions.Item>
      </Descriptions>
      <Button danger onClick={onDelete}>Delete</Button>
    </Card>
  );
};

// UserProfileContainer.tsx
const UserProfileContainer = () => {
  const { id } = useParams<{ id: string }>();
  const props = useUserProfile(id);
  return <UserProfilePresenter {...props} />;
};
```
