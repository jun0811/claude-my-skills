---
title: One Function, One Job
impact: MEDIUM
tags: readability, SRP, function
---

## One Function, One Job

If a function does more than one thing, split it. A good function fits in your head — typically under 20 lines of logic. Each extracted function should have a name that describes its single responsibility.

**Incorrect (one giant handler doing validation, API call, state updates, and navigation):**

```tsx
const handleSubmit = async (values: FormValues) => {
  if (!values.name.trim()) {
    setError('name', 'Name is required');
    return;
  }
  if (values.email && !EMAIL_REGEX.test(values.email)) {
    setError('email', 'Invalid email format');
    return;
  }
  if (values.password.length < 8) {
    setError('password', 'Password must be at least 8 characters');
    return;
  }
  setIsSubmitting(true);
  try {
    const payload = {
      ...values,
      name: values.name.trim(),
      email: values.email.toLowerCase(),
      createdAt: new Date().toISOString(),
    };
    const res = await api.post('/users', payload);
    setUsers((prev) => [...prev, res.data]);
    message.success('User created successfully');
    form.resetFields();
    navigate(`/users/${res.data.id}`);
  } catch (e) {
    message.error('Failed to create user');
  } finally {
    setIsSubmitting(false);
  }
};
```

**Correct (each step is a named function with a single responsibility):**

```tsx
const validateForm = (values: FormValues): string | null => {
  if (!values.name.trim()) return 'Name is required';
  if (values.email && !EMAIL_REGEX.test(values.email)) return 'Invalid email format';
  if (values.password.length < 8) return 'Password must be at least 8 characters';
  return null;
};

const buildCreatePayload = (values: FormValues): CreateUserPayload => ({
  ...values,
  name: values.name.trim(),
  email: values.email.toLowerCase(),
  createdAt: new Date().toISOString(),
});

const handleSubmit = async (values: FormValues) => {
  const validationError = validateForm(values);
  if (validationError) {
    message.error(validationError);
    return;
  }

  setIsSubmitting(true);
  try {
    const payload = buildCreatePayload(values);
    const newUser = await createUser(payload);
    setUsers((prev) => [...prev, newUser]);
    message.success('User created successfully');
    form.resetFields();
    navigate(`/users/${newUser.id}`);
  } catch {
    message.error('Failed to create user');
  } finally {
    setIsSubmitting(false);
  }
};
```
