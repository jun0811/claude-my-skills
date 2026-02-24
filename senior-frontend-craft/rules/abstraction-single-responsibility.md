---
title: One Module, One Reason to Change
impact: HIGH
tags: abstraction, SRP, SOLID
---

## One Module, One Reason to Change

Each module (file, function, class, hook) should have exactly one reason to change. If you need to modify a module for two unrelated features, split it. A hook that handles authentication AND user profile fetching will break when either auth flow or profile schema changes.

**Incorrect (one hook doing multiple unrelated jobs):**

```tsx
function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [notifications, setNotifications] = useState<Notification[]>([]);

  // Reason to change #1: auth flow changes
  const login = async (credentials: Credentials) => {
    const res = await authApi.login(credentials);
    setToken(res.token);
    setUser(res.user);
    // Also fetching profile here — tightly coupled
    const profileRes = await profileApi.get(res.user.id);
    setProfile(profileRes);
    // Also fetching notifications — completely unrelated
    const notifs = await notificationApi.list(res.user.id);
    setNotifications(notifs);
  };

  // Reason to change #2: token refresh strategy changes
  const refreshToken = async () => { /* ... */ };

  // Reason to change #3: profile schema or endpoint changes
  const updateProfile = async (data: Partial<UserProfile>) => { /* ... */ };

  // Reason to change #4: notification logic changes
  const markAsRead = async (id: string) => { /* ... */ };

  return { user, token, profile, notifications, login, refreshToken, updateProfile, markAsRead };
}
```

**Correct (separate hooks, each with one reason to change):**

```tsx
// Changes only when auth flow changes (login, logout, token strategy)
function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);

  const login = async (credentials: Credentials) => {
    const res = await authApi.login(credentials);
    setToken(res.token);
    setUser(res.user);
  };

  const logout = async () => {
    await authApi.logout();
    setToken(null);
    setUser(null);
  };

  const refreshToken = async () => {
    const res = await authApi.refresh(token);
    setToken(res.token);
  };

  return { user, token, isAuthenticated: !!token, login, logout, refreshToken };
}

// Changes only when profile schema or endpoint changes
function useUserProfile(userId: string | undefined) {
  const [profile, setProfile] = useState<UserProfile | null>(null);

  useEffect(() => {
    if (!userId) return;
    profileApi.get(userId).then(setProfile);
  }, [userId]);

  const updateProfile = async (data: Partial<UserProfile>) => {
    if (!userId) return;
    const updated = await profileApi.update(userId, data);
    setProfile(updated);
  };

  return { profile, updateProfile };
}

// Consumer composes what it needs
function DashboardPage() {
  const { user, isAuthenticated } = useAuth();
  const { profile } = useUserProfile(user?.id);

  if (!isAuthenticated) return <Redirect to="/login" />;
  return <Dashboard user={user!} profile={profile} />;
}
```
