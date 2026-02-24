# Infinite Query Patterns

Patterns for pagination and infinite scrolling with React Query v5.

## Basic Infinite Query

Load more data as user scrolls.

```typescript
function useInfiniteUserList() {
  return useInfiniteQuery({
    queryKey: userKeys.lists(),
    queryFn: ({ pageParam = 0 }) => fetchUsers({ 
      page: pageParam,
      limit: 20 
    }),
    getNextPageParam: (lastPage, allPages) => {
      // Return next page number or undefined if no more pages
      return lastPage.hasMore ? allPages.length : undefined;
    },
    initialPageParam: 0,
  });
}

// Usage
function UserList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteUserList();

  return (
    <div>
      {data?.pages.map((page, i) => (
        <React.Fragment key={i}>
          {page.users.map(user => (
            <UserCard key={user.id} user={user} />
          ))}
        </React.Fragment>
      ))}
      
      {hasNextPage && (
        <button 
          onClick={() => fetchNextPage()}
          disabled={isFetchingNextPage}
        >
          {isFetchingNextPage ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  );
}
```

## Infinite Query with Suspense

Use with React 18 Suspense.

```typescript
function UserInfiniteList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useSuspenseInfiniteQuery({
    queryKey: userKeys.lists(),
    queryFn: ({ pageParam }) => fetchUsers({ 
      page: pageParam,
      limit: 20 
    }),
    getNextPageParam: (lastPage) => lastPage.nextCursor,
    initialPageParam: 0,
  });

  // No loading state needed - handled by Suspense
  return (
    <div>
      {data.pages.flatMap(page => page.users).map(user => (
        <UserCard key={user.id} user={user} />
      ))}
      
      {hasNextPage && (
        <LoadMoreButton 
          onClick={fetchNextPage}
          isLoading={isFetchingNextPage}
        />
      )}
    </div>
  );
}
```

## Cursor-based Pagination

More reliable than offset pagination.

```typescript
interface PageResponse {
  users: User[];
  nextCursor?: string;
}

function useInfiniteUsers() {
  return useInfiniteQuery<PageResponse>({
    queryKey: userKeys.lists(),
    queryFn: ({ pageParam }) => fetchUsers({ 
      cursor: pageParam 
    }),
    getNextPageParam: (lastPage) => lastPage.nextCursor,
    initialPageParam: undefined,
  });
}
```

## Bidirectional Infinite Query

Load both previous and next pages.

```typescript
function useBidirectionalMessages(initialMessageId: string) {
  return useInfiniteQuery({
    queryKey: messageKeys.thread(threadId),
    queryFn: ({ pageParam }) => fetchMessages({
      cursor: pageParam.cursor,
      direction: pageParam.direction,
    }),
    getNextPageParam: (lastPage) => 
      lastPage.hasNext 
        ? { cursor: lastPage.nextCursor, direction: 'next' }
        : undefined,
    getPreviousPageParam: (firstPage) =>
      firstPage.hasPrev
        ? { cursor: firstPage.prevCursor, direction: 'prev' }
        : undefined,
    initialPageParam: { cursor: initialMessageId, direction: 'next' },
  });
}

// Usage
function MessageThread() {
  const {
    data,
    fetchNextPage,
    fetchPreviousPage,
    hasNextPage,
    hasPreviousPage,
  } = useBidirectionalMessages(initialMessageId);

  return (
    <div>
      {hasPreviousPage && (
        <button onClick={() => fetchPreviousPage()}>
          Load Previous
        </button>
      )}
      
      {data?.pages.map((page, i) => (
        <React.Fragment key={i}>
          {page.messages.map(msg => (
            <Message key={msg.id} message={msg} />
          ))}
        </React.Fragment>
      ))}
      
      {hasNextPage && (
        <button onClick={() => fetchNextPage()}>
          Load Next
        </button>
      )}
    </div>
  );
}
```

## Auto-scroll with Intersection Observer

Automatically load more when scrolling to bottom.

```typescript
function AutoLoadUserList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteUserList();

  const observerTarget = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasNextPage && !isFetchingNextPage) {
          fetchNextPage();
        }
      },
      { threshold: 0.1 }
    );

    const currentTarget = observerTarget.current;
    if (currentTarget) {
      observer.observe(currentTarget);
    }

    return () => {
      if (currentTarget) {
        observer.unobserve(currentTarget);
      }
    };
  }, [fetchNextPage, hasNextPage, isFetchingNextPage]);

  return (
    <div>
      {data?.pages.flatMap(page => page.users).map(user => (
        <UserCard key={user.id} user={user} />
      ))}
      
      <div ref={observerTarget}>
        {isFetchingNextPage && <LoadingSpinner />}
      </div>
    </div>
  );
}
```

## Refetch Infinite Query

Refetch all pages or specific pages.

```typescript
function UserListWithRefresh() {
  const queryClient = useQueryClient();
  const infiniteQuery = useInfiniteUserList();

  const refreshAll = () => {
    // Refetch all loaded pages
    infiniteQuery.refetch();
  };

  const refreshFirst = () => {
    // Invalidate to refetch only first page
    queryClient.invalidateQueries({ 
      queryKey: userKeys.lists(),
      refetchType: 'active',
    });
  };

  return (
    <div>
      <button onClick={refreshAll}>Refresh All</button>
      <button onClick={refreshFirst}>Refresh First Page</button>
      {/* list content */}
    </div>
  );
}
```

## Search with Infinite Query

Combine search filters with infinite scrolling.

```typescript
function useInfiniteSearchUsers(searchTerm: string) {
  return useInfiniteQuery({
    queryKey: userKeys.search(searchTerm),
    queryFn: ({ pageParam = 0 }) => searchUsers({ 
      query: searchTerm,
      page: pageParam,
      limit: 20 
    }),
    getNextPageParam: (lastPage, allPages) => 
      lastPage.hasMore ? allPages.length : undefined,
    initialPageParam: 0,
    enabled: searchTerm.length > 0, // Only search if term exists
  });
}

// Usage
function SearchableUserList() {
  const [search, setSearch] = useState('');
  const debouncedSearch = useDebounce(search, 300);
  
  const {
    data,
    fetchNextPage,
    hasNextPage,
  } = useInfiniteSearchUsers(debouncedSearch);

  return (
    <div>
      <input 
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Search users..."
      />
      
      {data?.pages.flatMap(page => page.users).map(user => (
        <UserCard key={user.id} user={user} />
      ))}
      
      {hasNextPage && (
        <button onClick={() => fetchNextPage()}>
          Load More
        </button>
      )}
    </div>
  );
}
```

## Optimistic Updates with Infinite Query

Add new item to infinite list optimistically.

```typescript
function useCreatePost() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createPost,
    
    onMutate: async (newPost) => {
      await queryClient.cancelQueries({ queryKey: postKeys.lists() });

      const previous = queryClient.getQueryData(postKeys.lists());

      // Add to first page optimistically
      queryClient.setQueryData(
        postKeys.lists(),
        (old: InfiniteData<PostPage>) => ({
          pages: [
            {
              posts: [newPost, ...(old.pages[0]?.posts ?? [])],
              hasMore: old.pages[0]?.hasMore ?? true,
            },
            ...old.pages.slice(1),
          ],
          pageParams: old.pageParams,
        })
      );

      return { previous };
    },

    onError: (err, newPost, context) => {
      if (context?.previous) {
        queryClient.setQueryData(postKeys.lists(), context.previous);
      }
    },

    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: postKeys.lists() });
    },
  });
}
```

## Virtual Scrolling with Infinite Query

Combine with react-window for performance.

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualizedUserList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
  } = useInfiniteUserList();

  const allRows = data?.pages.flatMap(page => page.users) ?? [];
  
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: allRows.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 100, // Estimated item height
    overscan: 5,
  });

  useEffect(() => {
    const [lastItem] = [...virtualizer.getVirtualItems()].reverse();

    if (!lastItem) return;

    if (
      lastItem.index >= allRows.length - 1 &&
      hasNextPage &&
      !isFetchingNextPage
    ) {
      fetchNextPage();
    }
  }, [
    hasNextPage,
    fetchNextPage,
    allRows.length,
    virtualizer.getVirtualItems(),
  ]);

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px` }}>
        {virtualizer.getVirtualItems().map((virtualRow) => {
          const user = allRows[virtualRow.index];
          return (
            <div
              key={virtualRow.key}
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: `${virtualRow.size}px`,
                transform: `translateY(${virtualRow.start}px)`,
              }}
            >
              <UserCard user={user} />
            </div>
          );
        })}
      </div>
    </div>
  );
}
```
