---
title: Reduce Nesting with Early Returns
impact: MEDIUM
tags: readability, nesting, guard-clause
---

## Reduce Nesting with Early Returns

Use early returns to handle edge cases first, keeping the main logic at the lowest nesting level. Deep nesting forces readers to maintain a mental stack of conditions — early returns flatten the logic and make it scannable.

**Incorrect (deeply nested conditionals — main logic buried at level 3+):**

```tsx
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error } = useUser(userId);

  if (!isLoading) {
    if (!error) {
      if (user) {
        if (user.isActive) {
          return (
            <div>
              <h1>{user.name}</h1>
              <p>{user.email}</p>
              {user.hasPermission('admin') ? (
                <AdminPanel user={user} />
              ) : (
                <p>Standard user</p>
              )}
            </div>
          );
        } else {
          return <InactiveAccount />;
        }
      } else {
        return <NotFound />;
      }
    } else {
      return <ErrorMessage error={error} />;
    }
  } else {
    return <Spinner />;
  }
}
```

**Correct (early returns for edge cases — main logic is at the top level):**

```tsx
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error } = useUser(userId);

  if (isLoading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!user) return <NotFound />;
  if (!user.isActive) return <InactiveAccount />;

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
      {user.hasPermission('admin') ? <AdminPanel user={user} /> : <p>Standard user</p>}
    </div>
  );
}
```
