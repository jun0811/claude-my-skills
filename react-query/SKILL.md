---
name: react-query
description: React Query (TanStack Query) v5 implementation guide for TypeScript projects. Use when implementing server state management, data fetching, caching strategies, or when users ask about React Query setup, useQuery, useMutation, Suspense integration, Error Boundary patterns, Optimistic Updates, or Query Key management.
---

# React Query v5 Implementation Guide

Complete guide for implementing React Query v5 with TypeScript, focusing on modern patterns including Suspense, Error Boundaries, and type-safe Query Key Factories.

## Quick Start

### 1. Installation

```bash
npm install @tanstack/react-query@^5
npm install @tanstack/react-query-devtools@^5
```

### 2. QueryClient Setup

```typescript
// src/lib/queryClient.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60, // 1 minute
      gcTime: 1000 * 60 * 5, // 5 minutes (formerly cacheTime)
      retry: 1,
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 0,
    },
  },
});
```

### 3. Provider Setup with Suspense & Error Boundary

```typescript
// src/App.tsx
import { QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { ErrorBoundary } from 'react-error-boundary';
import { Suspense } from 'react';
import { queryClient } from './lib/queryClient';

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ErrorBoundary fallback={<ErrorFallback />}>
        <Suspense fallback={<LoadingFallback />}>
          <YourApp />
        </Suspense>
      </ErrorBoundary>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

## Query Key Factory Pattern

Use hierarchical Query Key Factory pattern for type-safe, maintainable key management.

### Basic Structure

```typescript
// src/queries/keys/userKeys.ts
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters?: UserFilters) => [...userKeys.lists(), { filters }] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: number) => [...userKeys.details(), id] as const,
} as const;
```

### Benefits

- **Invalidation Control**: `queryClient.invalidateQueries({ queryKey: userKeys.all })` invalidates all user-related queries
- **Type Safety**: TypeScript ensures consistent key structure
- **Auto-completion**: IDE suggestions for all key variations
- **Prevents Typos**: Centralized key management

### Invalidation Examples

```typescript
// Invalidate all user queries (lists + details)
queryClient.invalidateQueries({ queryKey: userKeys.all });

// Invalidate only user lists
queryClient.invalidateQueries({ queryKey: userKeys.lists() });

// Invalidate specific user detail
queryClient.invalidateQueries({ queryKey: userKeys.detail(userId) });
```

## Core Patterns

### Use Suspense Query (Recommended for React 18)

```typescript
import { useSuspenseQuery } from '@tanstack/react-query';

function UserProfile({ userId }: { userId: number }) {
  // No loading state needed - handled by Suspense
  const { data } = useSuspenseQuery({
    queryKey: userKeys.detail(userId),
    queryFn: () => fetchUser(userId),
  });

  return <div>{data.name}</div>;
}
```

### Use Query (Traditional Pattern)

```typescript
function UserProfile({ userId }: { userId: number }) {
  const { data, isLoading, error } = useQuery({
    queryKey: userKeys.detail(userId),
    queryFn: () => fetchUser(userId),
  });

  if (isLoading) return <Loading />;
  if (error) return <Error error={error} />;
  
  return <div>{data.name}</div>;
}
```

### Mutations with Optimistic Updates

```typescript
function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (user: UpdateUserDto) => updateUser(user),
    
    // Optimistic update
    onMutate: async (newUser) => {
      await queryClient.cancelQueries({ queryKey: userKeys.detail(newUser.id) });
      
      const previous = queryClient.getQueryData(userKeys.detail(newUser.id));
      
      queryClient.setQueryData(userKeys.detail(newUser.id), newUser);
      
      return { previous };
    },
    
    // Rollback on error
    onError: (err, newUser, context) => {
      if (context?.previous) {
        queryClient.setQueryData(userKeys.detail(newUser.id), context.previous);
      }
    },
    
    // Always refetch after error or success
    onSettled: (data, error, variables) => {
      queryClient.invalidateQueries({ queryKey: userKeys.detail(variables.id) });
    },
  });
}
```

## Implementation Checklist

### Queries
- [ ] Query Key Factory created for each domain
- [ ] Using `as const` for type safety
- [ ] Hierarchical structure (all → lists/details → specific)
- [ ] Suspense Query used where appropriate
- [ ] Error boundaries configured
- [ ] Stale time configured appropriately
- [ ] TypeScript types defined for query responses

### Mutations
- [ ] Optimistic updates implemented where needed
- [ ] Error rollback logic in place
- [ ] Invalidation on success
- [ ] Success/error callbacks defined
- [ ] Retry configuration appropriate
- [ ] Loading states managed

### Performance
- [ ] Only necessary data refetched
- [ ] Query keys properly scoped
- [ ] GC time (gcTime) configured
- [ ] Prefetching used where beneficial
- [ ] Devtools enabled in development

## Advanced Patterns

For detailed implementation guides, see:

- **Query Patterns**: `references/query-patterns.md` - Detailed useQuery, useSuspenseQuery, dependent queries
- **Mutation Patterns**: `references/mutation-patterns.md` - Optimistic updates, error handling, complex mutations
- **Infinite Queries**: `references/infinite-query.md` - Pagination and infinite scroll
- **TypeScript Tips**: `references/typescript-tips.md` - Advanced typing patterns

## Common Pitfalls

1. **Not using Query Key Factory**: Leads to key inconsistencies and invalidation issues
2. **Over-fetching**: Not scoping query keys properly
3. **Missing error handling**: Not wrapping with Error Boundary or handling errors in queries
4. **Ignoring staleTime**: Default is 0, causing excessive refetches
5. **Not using Optimistic Updates**: Poor UX for mutations
