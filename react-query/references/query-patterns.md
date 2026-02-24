# Query Patterns

Advanced patterns for data fetching with React Query v5.

## useSuspenseQuery (React 18+)

Recommended pattern for new code with React 18. Eliminates loading state management.

### Basic Usage

```typescript
import { useSuspenseQuery } from '@tanstack/react-query';

function UserProfile({ userId }: { userId: number }) {
  const { data } = useSuspenseQuery({
    queryKey: userKeys.detail(userId),
    queryFn: () => fetchUser(userId),
  });

  // data is always defined, no need for loading/error checks
  return <div>{data.name}</div>;
}
```

### With Error Boundary

```typescript
function UserProfilePage({ userId }: { userId: number }) {
  return (
    <ErrorBoundary fallback={<UserErrorFallback />}>
      <Suspense fallback={<UserSkeleton />}>
        <UserProfile userId={userId} />
      </Suspense>
    </ErrorBoundary>
  );
}
```

## useQuery (Traditional)

Use when you need explicit control over loading/error states.

### Basic Usage

```typescript
function UserList() {
  const { data, isLoading, error, isFetching } = useQuery({
    queryKey: userKeys.lists(),
    queryFn: fetchUsers,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  
  return (
    <>
      {isFetching && <RefreshIndicator />}
      <UserTable users={data} />
    </>
  );
}
```

### With Filters

```typescript
function FilteredUserList({ filters }: { filters: UserFilters }) {
  const { data } = useQuery({
    queryKey: userKeys.list(filters),
    queryFn: () => fetchUsers(filters),
    // Only run query if filters are provided
    enabled: Boolean(filters),
  });

  return data ? <UserTable users={data} /> : <EmptyState />;
}
```

## Dependent Queries

Query that depends on data from another query.

```typescript
function UserPosts({ userId }: { userId: number }) {
  // First query
  const { data: user } = useSuspenseQuery({
    queryKey: userKeys.detail(userId),
    queryFn: () => fetchUser(userId),
  });

  // Second query depends on first
  const { data: posts } = useSuspenseQuery({
    queryKey: postKeys.byUser(user.id),
    queryFn: () => fetchUserPosts(user.id),
    // Only fetch if user exists
    enabled: !!user,
  });

  return <PostList posts={posts} />;
}
```

## Parallel Queries

Execute multiple queries simultaneously.

```typescript
function Dashboard() {
  const userQuery = useSuspenseQuery({
    queryKey: userKeys.detail(userId),
    queryFn: () => fetchUser(userId),
  });

  const statsQuery = useSuspenseQuery({
    queryKey: statsKeys.all,
    queryFn: fetchStats,
  });

  const notificationsQuery = useSuspenseQuery({
    queryKey: notificationKeys.lists(),
    queryFn: fetchNotifications,
  });

  return (
    <div>
      <UserHeader user={userQuery.data} />
      <StatsPanel stats={statsQuery.data} />
      <Notifications items={notificationsQuery.data} />
    </div>
  );
}
```

## Prefetching

Improve UX by prefetching data before navigation.

```typescript
function UserListItem({ user }: { user: User }) {
  const queryClient = useQueryClient();

  const prefetchUser = () => {
    queryClient.prefetchQuery({
      queryKey: userKeys.detail(user.id),
      queryFn: () => fetchUser(user.id),
      staleTime: 1000 * 60 * 5, // 5 minutes
    });
  };

  return (
    <Link 
      to={`/users/${user.id}`}
      onMouseEnter={prefetchUser}
      onFocus={prefetchUser}
    >
      {user.name}
    </Link>
  );
}
```

## Polling / Auto-refetch

Automatically refetch data at intervals.

```typescript
function RealtimeStats() {
  const { data } = useQuery({
    queryKey: statsKeys.realtime(),
    queryFn: fetchRealtimeStats,
    refetchInterval: 1000 * 10, // Every 10 seconds
    refetchIntervalInBackground: true, // Continue polling when tab is inactive
  });

  return <StatsDisplay stats={data} />;
}
```

## Initial Data

Provide initial data to avoid loading state.

```typescript
function UserProfile({ userId, cachedUser }: Props) {
  const { data } = useSuspenseQuery({
    queryKey: userKeys.detail(userId),
    queryFn: () => fetchUser(userId),
    initialData: cachedUser, // Use cached data initially
    staleTime: 1000 * 60, // Consider fresh for 1 minute
  });

  return <UserCard user={data} />;
}
```

## Placeholder Data

Show temporary data while loading.

```typescript
function UserList({ previousData }: { previousData?: User[] }) {
  const { data } = useQuery({
    queryKey: userKeys.lists(),
    queryFn: fetchUsers,
    placeholderData: previousData, // Show previous data while loading new
  });

  return <UserTable users={data} />;
}
```

## Select / Transform Data

Transform query data before returning.

```typescript
function UserNames() {
  const { data: names } = useQuery({
    queryKey: userKeys.lists(),
    queryFn: fetchUsers,
    select: (users) => users.map(user => user.name), // Transform data
  });

  return <NameList names={names} />;
}
```

## Status-based Rendering

Fine-grained control over different states.

```typescript
function UserProfile({ userId }: { userId: number }) {
  const { data, status, fetchStatus } = useQuery({
    queryKey: userKeys.detail(userId),
    queryFn: () => fetchUser(userId),
  });

  if (status === 'pending') return <Skeleton />;
  if (status === 'error') return <ErrorPage />;
  
  return (
    <>
      {fetchStatus === 'fetching' && <RefreshingIndicator />}
      <UserCard user={data} />
    </>
  );
}
```
