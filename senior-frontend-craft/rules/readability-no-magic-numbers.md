---
title: Extract Magic Numbers to Named Constants
impact: MEDIUM
tags: readability, constants, magic-numbers
---

## Extract Magic Numbers to Named Constants

Unnamed numeric or string literals hide meaning and make code harder to maintain. Extract them to named constants that explain intent. When the value needs to change, you update it in one place.

**Incorrect (raw literals scattered through the code — meaning is opaque):**

```tsx
function useSessionTimeout() {
  const [remaining, setRemaining] = useState(3600);

  useEffect(() => {
    const timer = setInterval(() => {
      setRemaining((prev) => {
        if (prev <= 0) {
          logout();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  if (remaining < 300) {
    message.warning('Session expiring soon');
  }

  // What is 86400000? What is 3? What is 5?
  const isStale = Date.now() - lastActivity > 86400000;
  const shouldRetry = retryCount < 3;
  const pageSize = 5;
}
```

**Correct (named constants reveal purpose — easy to understand and maintain):**

```tsx
const SESSION_CONFIG = {
  TIMEOUT_SECONDS: 60 * 60, // 1 hour
  WARNING_THRESHOLD_SECONDS: 5 * 60, // 5 minutes
  TICK_INTERVAL_MS: 1_000,
} as const;

const MAX_RETRIES = 3;
const ONE_DAY_MS = 24 * 60 * 60 * 1_000;
const DEFAULT_PAGE_SIZE = 5;

function useSessionTimeout() {
  const [remaining, setRemaining] = useState(SESSION_CONFIG.TIMEOUT_SECONDS);

  useEffect(() => {
    const timer = setInterval(() => {
      setRemaining((prev) => {
        if (prev <= 0) {
          logout();
          return 0;
        }
        return prev - 1;
      });
    }, SESSION_CONFIG.TICK_INTERVAL_MS);

    return () => clearInterval(timer);
  }, []);

  if (remaining < SESSION_CONFIG.WARNING_THRESHOLD_SECONDS) {
    message.warning('Session expiring soon');
  }

  const isStale = Date.now() - lastActivity > ONE_DAY_MS;
  const shouldRetry = retryCount < MAX_RETRIES;
}
```
