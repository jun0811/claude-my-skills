# Mutation Patterns

Patterns for data mutations with React Query v5, including optimistic updates and error handling.

## Basic Mutation

Simple mutation without optimistic updates.

```typescript
function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (newUser: CreateUserDto) => createUser(newUser),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
}

// Usage
function CreateUserForm() {
  const createUser = useCreateUser();

  const handleSubmit = (data: CreateUserDto) => {
    createUser.mutate(data, {
      onSuccess: (newUser) => {
        toast.success(`Created user: ${newUser.name}`);
        navigate(`/users/${newUser.id}`);
      },
      onError: (error) => {
        toast.error(`Failed: ${error.message}`);
      },
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* form fields */}
      <button disabled={createUser.isPending}>
        {createUser.isPending ? 'Creating...' : 'Create User'}
      </button>
    </form>
  );
}
```

## Optimistic Update (Single Item)

Update UI immediately, rollback on error.

```typescript
function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (user: UpdateUserDto) => updateUser(user),
    
    onMutate: async (updatedUser) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ 
        queryKey: userKeys.detail(updatedUser.id) 
      });

      // Snapshot previous value
      const previous = queryClient.getQueryData(
        userKeys.detail(updatedUser.id)
      );

      // Optimistically update
      queryClient.setQueryData(
        userKeys.detail(updatedUser.id),
        updatedUser
      );

      // Return context for rollback
      return { previous, updatedUser };
    },

    onError: (err, updatedUser, context) => {
      // Rollback on error
      if (context?.previous) {
        queryClient.setQueryData(
          userKeys.detail(updatedUser.id),
          context.previous
        );
      }
      toast.error(`Update failed: ${err.message}`);
    },

    onSettled: (data, error, variables) => {
      // Always refetch after mutation
      queryClient.invalidateQueries({ 
        queryKey: userKeys.detail(variables.id) 
      });
    },
  });
}
```

## Optimistic Update (List)

Update list items optimistically.

```typescript
function useDeleteUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (userId: number) => deleteUser(userId),
    
    onMutate: async (deletedId) => {
      await queryClient.cancelQueries({ queryKey: userKeys.lists() });

      const previous = queryClient.getQueryData(userKeys.lists());

      // Remove from list optimistically
      queryClient.setQueryData<User[]>(
        userKeys.lists(),
        (old) => old?.filter(user => user.id !== deletedId) ?? []
      );

      return { previous };
    },

    onError: (err, deletedId, context) => {
      if (context?.previous) {
        queryClient.setQueryData(userKeys.lists(), context.previous);
      }
    },

    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
}
```

## Optimistic Update (Add to List)

Add new item to list optimistically.

```typescript
function useCreateTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (newTodo: CreateTodoDto) => createTodo(newTodo),
    
    onMutate: async (newTodo) => {
      await queryClient.cancelQueries({ queryKey: todoKeys.lists() });

      const previous = queryClient.getQueryData(todoKeys.lists());

      // Add optimistic todo with temporary ID
      const optimisticTodo: Todo = {
        id: Date.now(), // Temporary ID
        ...newTodo,
        completed: false,
      };

      queryClient.setQueryData<Todo[]>(
        todoKeys.lists(),
        (old) => [...(old ?? []), optimisticTodo]
      );

      return { previous, optimisticTodo };
    },

    onSuccess: (newTodo, variables, context) => {
      // Replace optimistic todo with real one
      queryClient.setQueryData<Todo[]>(
        todoKeys.lists(),
        (old) => old?.map(todo => 
          todo.id === context.optimisticTodo.id ? newTodo : todo
        ) ?? []
      );
    },

    onError: (err, newTodo, context) => {
      if (context?.previous) {
        queryClient.setQueryData(todoKeys.lists(), context.previous);
      }
    },

    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: todoKeys.lists() });
    },
  });
}
```

## Multiple Mutations in Sequence

Chain mutations with proper error handling.

```typescript
function useUpdateUserProfile() {
  const queryClient = useQueryClient();
  const updateUser = useUpdateUser();
  const uploadAvatar = useUploadAvatar();

  const updateProfile = async (data: ProfileData) => {
    try {
      // First mutation
      const user = await updateUser.mutateAsync(data.user);
      
      // Second mutation (only if first succeeds)
      if (data.avatar) {
        await uploadAvatar.mutateAsync({
          userId: user.id,
          file: data.avatar,
        });
      }

      queryClient.invalidateQueries({ queryKey: userKeys.detail(user.id) });
      toast.success('Profile updated');
    } catch (error) {
      toast.error('Update failed');
      throw error;
    }
  };

  return {
    updateProfile,
    isPending: updateUser.isPending || uploadAvatar.isPending,
  };
}
```

## Parallel Mutations

Execute multiple mutations simultaneously.

```typescript
function useBulkUpdateUsers() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (users: UpdateUserDto[]) => {
      // Execute all mutations in parallel
      return Promise.all(
        users.map(user => updateUser(user))
      );
    },
    
    onSuccess: () => {
      // Invalidate all user queries
      queryClient.invalidateQueries({ queryKey: userKeys.all });
      toast.success('All users updated');
    },

    onError: (error) => {
      toast.error(`Bulk update failed: ${error.message}`);
    },
  });
}
```

## Mutation with File Upload

Handle file uploads with progress tracking.

```typescript
function useUploadFile() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ 
      file, 
      onProgress 
    }: { 
      file: File; 
      onProgress?: (progress: number) => void;
    }) => {
      const formData = new FormData();
      formData.append('file', file);

      return uploadFile(formData, {
        onUploadProgress: (progressEvent) => {
          const progress = progressEvent.total
            ? Math.round((progressEvent.loaded * 100) / progressEvent.total)
            : 0;
          onProgress?.(progress);
        },
      });
    },

    onSuccess: (uploadedFile) => {
      queryClient.invalidateQueries({ queryKey: fileKeys.lists() });
      toast.success('File uploaded');
    },
  });
}

// Usage
function FileUploader() {
  const [progress, setProgress] = useState(0);
  const uploadFile = useUploadFile();

  const handleUpload = (file: File) => {
    uploadFile.mutate({ 
      file, 
      onProgress: setProgress 
    });
  };

  return (
    <>
      <input type="file" onChange={(e) => handleUpload(e.target.files![0])} />
      {uploadFile.isPending && <ProgressBar value={progress} />}
    </>
  );
}
```

## Error Handling Patterns

Comprehensive error handling for mutations.

```typescript
function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createUser,
    
    onError: (error: ApiError, variables, context) => {
      // Log error
      console.error('User creation failed', { error, variables, context });

      // Handle specific error types
      if (error.status === 409) {
        toast.error('User already exists');
      } else if (error.status === 422) {
        toast.error('Invalid user data');
      } else {
        toast.error('Failed to create user. Please try again.');
      }

      // Report to error tracking
      trackError(error, { context: 'user-creation' });
    },

    onSuccess: (newUser) => {
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
      toast.success(`User ${newUser.name} created`);
    },

    // Retry configuration
    retry: (failureCount, error: ApiError) => {
      // Don't retry on client errors (4xx)
      if (error.status >= 400 && error.status < 500) {
        return false;
      }
      // Retry up to 3 times on server errors
      return failureCount < 3;
    },
  });
}
```

## Mutation State Management

Track mutation state globally.

```typescript
function MutationStatus() {
  const queryClient = useQueryClient();
  
  // Get all pending mutations
  const mutations = queryClient.getMutationCache().getAll();
  const hasPending = mutations.some(m => m.state.status === 'pending');

  if (hasPending) {
    return <GlobalLoadingIndicator />;
  }

  return null;
}
```
