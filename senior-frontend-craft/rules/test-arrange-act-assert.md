---
title: Structure Tests with AAA Pattern
impact: LOW-MEDIUM
tags: testing, AAA, structure
---

## Structure Tests with AAA Pattern

Every test should have three clear phases: Arrange (setup), Act (execute), Assert (verify). This consistent structure makes tests readable and easy to scan. When phases are jumbled, it becomes unclear what the test is actually verifying.

**Incorrect (setup, actions, and assertions mixed together — hard to follow):**

```tsx
it('should filter and display results', async () => {
  const mockUsers = [{ id: '1', name: 'Alice' }, { id: '2', name: 'Bob' }];
  render(<UserSearch />);
  expect(screen.getByPlaceholderText('Search')).toBeInTheDocument();
  server.use(http.get('/api/users', () => HttpResponse.json(mockUsers)));
  await userEvent.type(screen.getByPlaceholderText('Search'), 'Ali');
  expect(screen.getByText('Alice')).toBeInTheDocument();
  const clearBtn = screen.getByRole('button', { name: 'Clear' });
  expect(clearBtn).toBeEnabled();
  await userEvent.click(clearBtn);
  expect(screen.queryByText('Alice')).not.toBeInTheDocument();
  expect(screen.getByPlaceholderText('Search')).toHaveValue('');
});
```

**Correct (three distinct phases separated by blank lines — intent is immediately clear):**

```tsx
it('should show matching users when searching by name', async () => {
  // Arrange
  const mockUsers = [
    { id: '1', name: 'Alice' },
    { id: '2', name: 'Bob' },
  ];
  server.use(http.get('/api/users', () => HttpResponse.json(mockUsers)));
  render(<UserSearch />);

  // Act
  await userEvent.type(screen.getByPlaceholderText('Search'), 'Ali');

  // Assert
  expect(await screen.findByText('Alice')).toBeInTheDocument();
  expect(screen.queryByText('Bob')).not.toBeInTheDocument();
});

it('should clear search results when clear button is clicked', async () => {
  // Arrange
  server.use(http.get('/api/users', () => HttpResponse.json([{ id: '1', name: 'Alice' }])));
  render(<UserSearch />);
  await userEvent.type(screen.getByPlaceholderText('Search'), 'Ali');
  await screen.findByText('Alice');

  // Act
  await userEvent.click(screen.getByRole('button', { name: 'Clear' }));

  // Assert
  expect(screen.queryByText('Alice')).not.toBeInTheDocument();
  expect(screen.getByPlaceholderText('Search')).toHaveValue('');
});
```
