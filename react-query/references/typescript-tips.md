# TypeScript Tips

Advanced TypeScript patterns for type-safe React Query usage.

## Typed Query Keys

Define strict types for query keys.

```typescript
// src/queries/keys/userKeys.ts
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters?: UserFilters) => [...userKeys.lists(), { filters }] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: number) => [...userKeys.details(), id] as const,
} as const;

// Type for user query keys
type UserKeys = ReturnType<typeof userKeys[keyof typeof userKeys]>;
```

## Typed Query Functions

Ensure type safety between queryKey and queryFn.

```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

interface UserFilters {
  role?: string;
  status?: 'active' | 'inactive';
}

// Typed query function
async function fetchUser(userId: number): Promise<User> {
  const response = await api.get(`/users/${userId}`);
  return response.data;
}

async function fetchUsers(filters?: UserFilters): Promise<User[]> {
  const response = await api.get('/users', { params: filters });
  return response.data;
}

// Usage with full type safety
function useUser(userId: number) {
  return useSuspenseQuery({
    queryKey: userKeys.detail(userId),
    queryFn: () => fetchUser(userId), // Type-safe!
  });
}
```

## Generic Query Hook Factory

Create reusable typed query hooks.

```typescript
interface QueryConfig<TData, TParams> {
  keys: {
    all: readonly string[];
    detail: (params: TParams) => readonly unknown[];
  };
  fetcher: (params: TParams) => Promise<TData>;
}

function createDetailQuery<TData, TParams>(
  config: QueryConfig<TData, TParams>
) {
  return function useDetailQuery(params: TParams) {
    return useSuspenseQuery({
      queryKey: config.keys.detail(params),
      queryFn: () => config.fetcher(params),
    });
  };
}

// Usage
const useUser = createDetailQuery({
  keys: userKeys,
  fetcher: fetchUser,
});

const usePost = createDetailQuery({
  keys: postKeys,
  fetcher: fetchPost,
});
```

## Typed Mutation Functions

Full type safety for mutations.

```typescript
interface CreateUserDto {
  name: string;
  email: string;
  role: 'admin' | 'user';
}

interface UpdateUserDto {
  id: number;
  name?: string;
  email?: string;
}

async function createUser(data: CreateUserDto): Promise<User> {
  const response = await api.post('/users', data);
  return response.data;
}

async function updateUser(data: UpdateUserDto): Promise<User> {
  const response = await api.put(`/users/${data.id}`, data);
  return response.data;
}

function useCreateUser() {
  return useMutation({
    mutationFn: createUser,
    // Full type inference for callbacks
    onSuccess: (newUser: User) => {
      console.log('Created user:', newUser.name);
    },
  });
}
```

## Typed Error Handling

Type-safe error handling with discriminated unions.

```typescript
type ApiError =
  | { status: 400; code: 'VALIDATION_ERROR'; errors: ValidationError[] }
  | { status: 401; code: 'UNAUTHORIZED'; message: string }
  | { status: 404; code: 'NOT_FOUND'; resource: string }
  | { status: 500; code: 'INTERNAL_ERROR'; message: string };

interface ValidationError {
  field: string;
  message: string;
}

function useUser(userId: number) {
  return useQuery({
    queryKey: userKeys.detail(userId),
    queryFn: () => fetchUser(userId),
    // Type-safe error handling
    retry: (failureCount, error: ApiError) => {
      // TypeScript knows error structure
      if (error.status === 404) {
        return false; // Don't retry on 404
      }
      return failureCount < 3;
    },
  });
}

// Usage with error boundary
function ErrorFallback({ error }: { error: ApiError }) {
  if (error.status === 404) {
    return <NotFoundPage resource={error.resource} />;
  }
  if (error.status === 401) {
    return <UnauthorizedPage />;
  }
  return <GenericError message={error.message} />;
}
```

## Typed Query Data

Type-safe query data access.

```typescript
function useUserData(userId: number) {
  const queryClient = useQueryClient();

  const getUserData = () => {
    // Type-safe data access
    return queryClient.getQueryData<User>(userKeys.detail(userId));
  };

  const setUserData = (updater: (old: User) => User) => {
    queryClient.setQueryData<User>(
      userKeys.detail(userId),
      updater
    );
  };

  return { getUserData, setUserData };
}
```

## Typed Optimistic Updates

Full type safety for optimistic updates.

```typescript
interface OptimisticContext {
  previous: User | undefined;
  optimisticUser: User;
}

function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation<
    User,                    // Response type
    ApiError,                // Error type
    UpdateUserDto,           // Variables type
    OptimisticContext        // Context type
  >({
    mutationFn: updateUser,
    
    onMutate: async (updatedUser): Promise<OptimisticContext> => {
      await queryClient.cancelQueries({ 
        queryKey: userKeys.detail(updatedUser.id) 
      });

      const previous = queryClient.getQueryData<User>(
        userKeys.detail(updatedUser.id)
      );

      const optimisticUser: User = {
        ...previous!,
        ...updatedUser,
      };

      queryClient.setQueryData<User>(
        userKeys.detail(updatedUser.id),
        optimisticUser
      );

      return { previous, optimisticUser };
    },

    onError: (err, updatedUser, context) => {
      // All types are inferred!
      if (context?.previous) {
        queryClient.setQueryData(
          userKeys.detail(updatedUser.id),
          context.previous
        );
      }
    },
  });
}
```

## Strict Query Options

Enforce required options with TypeScript.

```typescript
import type { UseQueryOptions } from '@tanstack/react-query';

// Require staleTime for all user queries
type StrictUserQueryOptions<TData = User> = UseQueryOptions<TData> & {
  staleTime: number; // Required!
};

function useStrictUser(
  userId: number,
  options: StrictUserQueryOptions
) {
  return useQuery({
    queryKey: userKeys.detail(userId),
    queryFn: () => fetchUser(userId),
    ...options,
  });
}

// Usage - must provide staleTime
const { data } = useStrictUser(1, {
  staleTime: 1000 * 60, // Required!
});
```

## Typed Select

Type-safe data transformation.

```typescript
function useUserNames() {
  return useQuery({
    queryKey: userKeys.lists(),
    queryFn: fetchUsers,
    // Type-safe select with inference
    select: (users: User[]): string[] => {
      return users.map(user => user.name);
    },
  });
}

// Return type is automatically QueryObserverResult<string[]>
```

## Generic Infinite Query

Type-safe infinite query patterns.

```typescript
interface PaginatedResponse<T> {
  data: T[];
  nextCursor?: string;
  hasMore: boolean;
}

function useInfiniteData<T>(
  queryKey: readonly unknown[],
  fetcher: (cursor: string | undefined) => Promise<PaginatedResponse<T>>
) {
  return useInfiniteQuery({
    queryKey,
    queryFn: ({ pageParam }) => fetcher(pageParam),
    getNextPageParam: (lastPage) => lastPage.nextCursor,
    initialPageParam: undefined,
  });
}

// Usage
const usersQuery = useInfiniteData<User>(
  userKeys.lists(),
  (cursor) => fetchPaginatedUsers({ cursor })
);
```

## Zod Schema Validation

Runtime type validation with Zod.

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.number(),
  name: z.string(),
  email: z.string().email(),
  role: z.enum(['admin', 'user']),
});

type User = z.infer<typeof UserSchema>;

async function fetchUser(userId: number): Promise<User> {
  const response = await api.get(`/users/${userId}`);
  // Runtime validation
  return UserSchema.parse(response.data);
}

function useUser(userId: number) {
  return useSuspenseQuery({
    queryKey: userKeys.detail(userId),
    queryFn: () => fetchUser(userId),
    // Type is automatically inferred from schema
  });
}
```

## Custom Hooks with Generics

Reusable typed hooks.

```typescript
interface Entity {
  id: number;
}

interface EntityKeys<T extends Entity> {
  all: readonly string[];
  detail: (id: number) => readonly unknown[];
}

function useEntityDetail<T extends Entity>(
  id: number,
  keys: EntityKeys<T>,
  fetcher: (id: number) => Promise<T>
) {
  return useSuspenseQuery({
    queryKey: keys.detail(id),
    queryFn: () => fetcher(id),
  });
}

// Usage
interface Post extends Entity {
  title: string;
  content: string;
}

const postKeys: EntityKeys<Post> = {
  all: ['posts'],
  detail: (id) => [...postKeys.all, id],
};

const { data } = useEntityDetail(1, postKeys, fetchPost);
// data is typed as Post
```
