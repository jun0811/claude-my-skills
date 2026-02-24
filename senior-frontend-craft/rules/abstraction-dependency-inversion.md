---
title: Depend on Interfaces, Not Implementations
impact: HIGH
tags: abstraction, DIP, SOLID, decoupling
---

## Depend on Interfaces, Not Implementations

High-level modules (components, business logic) should not depend on low-level details (HTTP clients, storage APIs). Define interfaces or type contracts and depend on those, so you can swap implementations without changing consumers.

**Incorrect (component directly coupled to HTTP client and API details):**

```tsx
// Component knows about axios, endpoint URLs, response shapes, headers
import axios from 'axios';

function UserSettings() {
  const [settings, setSettings] = useState<Settings | null>(null);

  useEffect(() => {
    axios.get('/ixcloud-api/v2/users/settings', {
      headers: { 'X-Auth-Token': localStorage.getItem('token') },
    }).then(res => {
      // Knows about the raw API response shape
      setSettings({
        theme: res.data.user_settings.theme_preference,
        language: res.data.user_settings.lang_code,
        timezone: res.data.user_settings.tz,
      });
    });
  }, []);

  const updateTheme = async (theme: string) => {
    await axios.put('/ixcloud-api/v2/users/settings', {
      user_settings: { theme_preference: theme },
    });
    setSettings(prev => prev ? { ...prev, theme } : null);
  };

  if (!settings) return <Spin />;
  return <SettingsForm settings={settings} onChangeTheme={updateTheme} />;
}
```

**Correct (component depends on a typed hook interface, implementation details are hidden):**

```tsx
// 1. Define the contract (interface)
interface UseSettingsReturn {
  settings: Settings | null;
  loading: boolean;
  updateTheme: (theme: string) => Promise<void>;
  updateLanguage: (lang: string) => Promise<void>;
}

// 2. Implement the contract (low-level detail, hidden from consumers)
function useSettings(): UseSettingsReturn {
  const [settings, setSettings] = useState<Settings | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    settingsApi.get()
      .then(setSettings)
      .finally(() => setLoading(false));
  }, []);

  const updateTheme = async (theme: string) => {
    await settingsApi.updateTheme(theme);
    setSettings(prev => prev ? { ...prev, theme } : null);
  };

  const updateLanguage = async (lang: string) => {
    await settingsApi.updateLanguage(lang);
    setSettings(prev => prev ? { ...prev, language: lang } : null);
  };

  return { settings, loading, updateTheme, updateLanguage };
}

// 3. Component depends only on the hook's return type — no API details leak in
function UserSettings() {
  const { settings, loading, updateTheme } = useSettings();

  if (loading) return <Spin />;
  if (!settings) return <Empty description="Failed to load settings" />;

  return <SettingsForm settings={settings} onChangeTheme={updateTheme} />;
}

// Bonus: trivially testable — mock the hook, not axios
vi.mock('./useSettings', () => ({
  useSettings: () => ({
    settings: { theme: 'dark', language: 'ko' },
    loading: false,
    updateTheme: vi.fn(),
    updateLanguage: vi.fn(),
  }),
}));
```
