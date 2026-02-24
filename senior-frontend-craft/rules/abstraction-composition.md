---
title: Prefer Composition over Inheritance
impact: HIGH
tags: abstraction, composition, patterns
---

## Prefer Composition over Inheritance

Build complex behavior by combining simple, focused pieces rather than extending classes or stacking HOCs. Deep HOC chains obscure data flow, make debugging painful, and create implicit prop dependencies that are invisible at the call site.

**Incorrect (HOC pyramid — props become invisible, debugging is a nightmare):**

```tsx
// Each HOC injects props magically — impossible to trace data flow
const withAuth = (Component: React.FC<any>) => (props: any) => {
  const auth = useContext(AuthContext);
  return <Component {...props} user={auth.user} isAdmin={auth.isAdmin} />;
};

const withLoading = (Component: React.FC<any>) => (props: any) => {
  const [loading, setLoading] = useState(true);
  return loading ? <Spin /> : <Component {...props} loading={loading} />;
};

const withErrorHandler = (Component: React.FC<any>) => (props: any) => {
  const [error, setError] = useState<Error | null>(null);
  if (error) return <ErrorDisplay error={error} />;
  return <Component {...props} onError={setError} />;
};

// Where does `user` come from? Where does `loading` come from?
// TypeScript can't infer the composed props correctly
export default withAuth(withLoading(withErrorHandler(InstanceList)));
```

**Correct (compose hooks inside the component — explicit data flow, full type safety):**

```tsx
// Each hook is independently typed, testable, and traceable
function useAuth() {
  const { user, isAdmin } = useContext(AuthContext);
  return { user, isAdmin };
}

function useInstanceList(projectId: string) {
  const [instances, setInstances] = useState<Instance[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    setLoading(true);
    instanceApi.list(projectId)
      .then(res => setInstances(res.data))
      .catch(setError)
      .finally(() => setLoading(false));
  }, [projectId]);

  return { instances, loading, error };
}

// All data sources are visible, typed, and debuggable
function InstanceList() {
  const { user, isAdmin } = useAuth();
  const { instances, loading, error } = useInstanceList(user.projectId);

  if (error) return <ErrorDisplay error={error} />;
  if (loading) return <Spin />;

  return (
    <Table
      dataSource={instances}
      columns={buildColumns({ isAdmin })}
    />
  );
}

// For shared UI wrappers, use compound components instead of HOCs
function PageShell({ children }: { children: React.ReactNode }) {
  return (
    <ErrorBoundary fallback={<ErrorDisplay />}>
      <Suspense fallback={<Spin />}>
        {children}
      </Suspense>
    </ErrorBoundary>
  );
}
```
