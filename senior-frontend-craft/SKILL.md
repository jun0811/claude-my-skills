---
name: senior-frontend-craft
description: Use when writing, reviewing, or refactoring frontend code — applies senior-level architecture, TypeScript, refactoring, and code quality patterns automatically.
---

# Senior Frontend Craft

Comprehensive code quality guide for frontend applications. Contains 36 rules across 8 categories, prioritized by impact. Apply these rules automatically when writing or reviewing code — explain violations with rule ID and reason.

## When to Apply

- Writing new components, hooks, or utilities
- Reviewing or refactoring existing code
- Designing component architecture or state management
- TypeScript type design decisions

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Architecture & Separation | CRITICAL | `arch-` |
| 2 | Refactoring Patterns | CRITICAL | `refactor-` |
| 3 | TypeScript Mastery | HIGH | `ts-` |
| 4 | Abstraction Design | HIGH | `abstraction-` |
| 5 | State Management | MEDIUM-HIGH | `state-` |
| 6 | Error Handling | MEDIUM | `error-` |
| 7 | Code Readability | MEDIUM | `readability-` |
| 8 | Testing Strategy | LOW-MEDIUM | `test-` |

## Quick Reference

### 1. Architecture & Separation (CRITICAL)

- `arch-container-presenter` - Separate data logic from UI rendering
- `arch-colocation` - Keep related code close together
- `arch-dependency-direction` - Dependencies flow inward only
- `arch-layer-boundary` - Respect API → Hook → Component layers
- `arch-barrel-exports` - Define public API via index.ts

### 2. Refactoring Patterns (CRITICAL)

- `refactor-extract-hook` - Extract data/state logic into custom hooks
- `refactor-extract-component` - Split large components by responsibility
- `refactor-parameter-object` - Group 3+ parameters into an object
- `refactor-replace-conditional` - Replace complex conditionals with map/strategy
- `refactor-single-pass` - Combine multiple iterations into one
- `refactor-remove-flag-args` - Eliminate boolean flag parameters

### 3. TypeScript Mastery (HIGH)

- `ts-discriminated-union` - Use discriminated unions for type-safe branching
- `ts-generic-constraints` - Constrain generics for better inference
- `ts-no-any` - Ban any, use unknown with type guards
- `ts-type-narrowing` - Leverage type narrowing over assertions
- `ts-utility-types` - Use built-in utility types effectively
- `ts-const-assertion` - Use as const for literal types and immutability

### 4. Abstraction Design (HIGH)

- `abstraction-rule-of-three` - Don't abstract before 3 repetitions
- `abstraction-single-responsibility` - One module, one reason to change
- `abstraction-composition` - Prefer composition over inheritance
- `abstraction-dependency-inversion` - Depend on interfaces, not implementations

### 5. State Management (MEDIUM-HIGH)

- `state-minimal` - Store only the minimum necessary state
- `state-derived` - Compute derived values, don't store them
- `state-colocation` - Place state closest to where it's used
- `state-immutable-update` - Always update state immutably

### 6. Error Handling (MEDIUM)

- `error-boundary` - Isolate failures with error boundaries
- `error-type-safe` - Type-safe error handling with Result pattern
- `error-fail-fast` - Validate early, fail immediately

### 7. Code Readability (MEDIUM)

- `readability-naming` - Names should reveal intent
- `readability-function-size` - One function, one job
- `readability-early-return` - Reduce nesting with early returns
- `readability-no-magic-numbers` - Extract magic numbers to named constants
- `readability-self-documenting` - Code should explain itself

### 8. Testing Strategy (LOW-MEDIUM)

- `test-behavior-not-impl` - Test what it does, not how it does it
- `test-arrange-act-assert` - Structure tests with AAA pattern
- `test-mock-boundaries` - Only mock at system boundaries

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/arch-container-presenter.md
rules/ts-discriminated-union.md
rules/refactor-extract-hook.md
```

Each rule contains: brief explanation, incorrect code example, correct code example.
