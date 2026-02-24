---
title: Test What It Does, Not How It Does It
impact: MEDIUM
tags: testing, behavior, implementation
---

## Test What It Does, Not How It Does It

Tests should verify outcomes and user-visible behavior, not internal implementation details. Implementation-coupled tests break during refactoring even when behavior is unchanged, creating maintenance burden without catching real bugs.

**Incorrect (testing internal state changes and method call order):**

```tsx
it('should load users', async () => {
  const setState = vi.fn();
  vi.spyOn(React, 'useState').mockReturnValue([[], setState]);
  const fetchSpy = vi.spyOn(api, 'fetchUsers');

  render(<UserList />);

  // Testing implementation: which functions were called, in what order, with what args
  expect(fetchSpy).toHaveBeenCalledTimes(1);
  expect(setState).toHaveBeenCalledWith(expect.any(Function));
  expect(setState).toHaveBeenNthCalledWith(1, expect.objectContaining({ loading: true }));
});

it('should handle click', () => {
  const onSelect = vi.fn();
  render(<UserCard user={mockUser} onSelect={onSelect} />);

  fireEvent.click(screen.getByRole('button'));

  // Testing that the exact callback was invoked with exact internal shape
  expect(onSelect).toHaveBeenCalledWith({ id: '1', _internal: true, _timestamp: expect.any(Number) });
});
```

**Correct (testing what the user sees and experiences):**

```tsx
it('should display users after loading', async () => {
  server.use(http.get('/api/users', () => HttpResponse.json([
    { id: '1', name: 'Alice' },
    { id: '2', name: 'Bob' },
  ])));

  render(<UserList />);

  // Verify loading state is shown to the user
  expect(screen.getByText('Loading...')).toBeInTheDocument();

  // Verify users appear after loading
  expect(await screen.findByText('Alice')).toBeInTheDocument();
  expect(screen.getByText('Bob')).toBeInTheDocument();
  expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
});

it('should show selected state when user card is clicked', async () => {
  render(<UserCard user={mockUser} onSelect={vi.fn()} />);

  await userEvent.click(screen.getByRole('button', { name: /Alice/ }));

  // Verify the visible outcome, not the internal mechanism
  expect(screen.getByRole('button', { name: /Alice/ })).toHaveClass('selected');
});
```
