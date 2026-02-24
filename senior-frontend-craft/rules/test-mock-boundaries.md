---
title: Only Mock at System Boundaries
impact: LOW-MEDIUM
tags: testing, mocking, boundaries
---

## Only Mock at System Boundaries

Mock external dependencies (API calls, browser APIs, third-party libraries), not your own code. Over-mocking internal modules makes tests brittle — they break when you refactor internals, even if the behavior is unchanged. Let your own code run so tests verify real integration.

**Incorrect (mocking internal utilities, custom hooks, and child components):**

```tsx
vi.mock('@/utils/formatDate', () => ({ formatDate: vi.fn(() => '2024-01-01') }));
vi.mock('@/hooks/usePermission', () => ({ usePermission: vi.fn(() => ({ canEdit: true })) }));
vi.mock('@/components/UserAvatar', () => ({ default: () => <div data-testid="avatar" /> }));

it('should render user details', () => {
  // Everything is faked — this test proves nothing about real behavior.
  // If formatDate signature changes, usePermission logic changes, or
  // UserAvatar props change, this test still passes silently.
  render(<UserDetail user={mockUser} />);

  expect(screen.getByTestId('avatar')).toBeInTheDocument();
  expect(screen.getByText('2024-01-01')).toBeInTheDocument();
});
```

**Correct (mock only external boundaries — let internal code run for real):**

```tsx
// Mock the system boundary: network requests
const server = setupServer(
  http.get('/api/users/:id', ({ params }) =>
    HttpResponse.json({ id: params.id, name: 'Alice', createdAt: '2024-01-15T00:00:00Z' }),
  ),
  http.get('/api/permissions', () =>
    HttpResponse.json({ canEdit: true, canDelete: false }),
  ),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Mock browser APIs when needed
const localStorageMock = vi.spyOn(Storage.prototype, 'getItem').mockReturnValue('token-123');

it('should render user details with formatted date and permissions', async () => {
  // Internal code (formatDate, usePermission, UserAvatar) runs for real.
  // Tests catch real integration issues.
  render(<UserDetail userId="1" />);

  expect(await screen.findByText('Alice')).toBeInTheDocument();
  expect(screen.getByText('January 15, 2024')).toBeInTheDocument(); // real formatDate output
  expect(screen.getByRole('button', { name: 'Edit' })).toBeEnabled(); // real permission check
  expect(screen.queryByRole('button', { name: 'Delete' })).not.toBeInTheDocument();
});
```
