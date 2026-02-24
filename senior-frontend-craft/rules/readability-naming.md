---
title: Names Should Reveal Intent
impact: MEDIUM
tags: readability, naming, clarity
---

## Names Should Reveal Intent

Variable, function, and component names should describe WHAT they represent or DO, not HOW they are implemented. A good name eliminates the need for a comment. Boolean variables start with `is/has/can/should`; event handlers start with `handle/on`.

**Incorrect (vague, abbreviated, or implementation-focused names):**

```tsx
function UserList() {
  const [d, setD] = useState<User[]>([]);
  const [flag, setFlag] = useState(false);
  const [val, setVal] = useState('');

  const getData = async () => {
    setFlag(true);
    const res = await api.get('/users');
    setD(res.data);
    setFlag(false);
  };

  const fn = (e: React.ChangeEvent<HTMLInputElement>) => {
    setVal(e.target.value);
  };

  const list = d.filter((x) => x.name.includes(val));

  return (
    <div>
      {flag && <Spinner />}
      <input onChange={fn} />
      {list.map((x) => <Card key={x.id} user={x} />)}
    </div>
  );
}
```

**Correct (names reveal purpose — code reads like prose):**

```tsx
function UserList() {
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchUsers = async () => {
    setIsLoading(true);
    const res = await api.get('/users');
    setUsers(res.data);
    setIsLoading(false);
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
  };

  const filteredUsers = users.filter((user) => user.name.includes(searchQuery));

  return (
    <div>
      {isLoading && <Spinner />}
      <input onChange={handleSearchChange} />
      {filteredUsers.map((user) => <Card key={user.id} user={user} />)}
    </div>
  );
}
```
