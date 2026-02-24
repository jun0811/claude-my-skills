---
name: react-testing-expert
description: Generates comprehensive unit and integration tests for React components using Vitest and React Testing Library. Use when creating new components, improving test coverage, or debugging failing tests.
allowed-tools: Read, Write, Grep, Glob
---

# React Testing Expert

This Skill enables Claude to write resilient and maintainable tests for React applications, focusing on user-centric testing patterns rather than implementation details.

## Instructions

1.  **Environment Detection**: Use `Read` to check the existing testing setup (e.g., `vitest.config.ts`, `jest.config.js`, or `setupTests.ts`) to match the project's syntax and matchers.
2.  **Test Strategy**:
    * Prioritize **React Testing Library (RTL)** for component tests.
    * Follow the **AAA Pattern**: Arrange (set up props/mocks), Act (interact with UI), Assert (verify outcomes).
    * Use `screen` queries that reflect user experience (e.g., `getByRole`, `getByLabelText`) over data-testids.
3.  **Mocking**:
    * Use `vi.mock()` for external modules or heavy dependencies.
    * Implement MSW (Mock Service Worker) patterns for API call interceptions if the project uses it.
4.  **Coverage**: Ensure edge cases (loading states, error boundaries, empty data) are covered.

## Best Practices

* **Avoid implementation details**: Don't test internal component state; test what the user sees on the screen.
* **Async Testing**: Always use `findBy*` queries or `waitFor` when dealing with asynchronous updates or API calls.
* **Accessibility Testing**: Use `jest-axe` if available to check for basic accessibility violations during tests.

## Test Writing Guidelines

### Testing a Counter Component

When writing a test for a Counter component that increments on button click:

1. **Import Statements**: Import render, screen, and fireEvent from @testing-library/react, and describe, it, expect from vitest. Import the component being tested.

2. **Test Structure**:
   - Create a describe block with the component name
   - Write an it block with a clear description of the expected behavior
   - Follow the AAA pattern throughout

3. **Arrange Phase**:
   - Call render with the component and any required props (e.g., initialValue)
   - Use screen.getByRole to locate the button with a regex pattern matching the button text
   - Use screen.getByText to find the initial count display

4. **Act Phase**:
   - Use fireEvent.click on the button element
   - Await the action if it triggers asynchronous updates

5. **Assert Phase**:
   - Use expect with screen.getByText to verify the updated count
   - Use .toBeInTheDocument() matcher to confirm presence

### Mocking an API Call

When testing a UserProfile component that fetches data on mount:

1. **Mock Setup**:
   - Use vi.mock to mock the API module path
   - Return an object with mocked functions
   - Use vi.fn().mockResolvedValue() for the fetch function
   - Provide mock data structure (e.g., object with name and email fields)

2. **Test Implementation**:
   - Import render and screen from testing library
   - Import the component and vi from vitest
   - Place the mock setup before the test block

3. **Async Assertions**:
   - Render the component with required props (e.g., userId)
   - Use screen.findByText for async queries (handles loading states automatically)
   - Await the findBy query result
   - Assert with .toBeInTheDocument()

## Troubleshooting

* If tests fail due to "Act" warnings, ensure all state updates are wrapped or awaited correctly.
* If `screen` is undefined, ensure `@testing-library/react` is correctly imported.

## Security Considerations

This skill reads existing test configuration files and writes new test files. It does not execute tests or modify application code. Mocked API responses are for testing purposes only and do not interact with real services.
