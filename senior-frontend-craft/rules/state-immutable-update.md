---
title: Always Update State Immutably
impact: MEDIUM-HIGH
tags: state, immutability, React
---

## Always Update State Immutably

Never mutate state objects or arrays directly. React relies on reference equality to detect changes -- mutating an existing object and passing it to setState will not trigger a re-render, leading to stale UI. Always create new references using spread, map, or filter.

**Incorrect (mutating state directly -- React won't detect the change):**

```tsx
function InstanceManager() {
  const [instances, setInstances] = useState<Instance[]>([]);

  const addInstance = (newInstance: Instance) => {
    // BUG: push mutates the existing array — same reference, no re-render
    instances.push(newInstance);
    setInstances(instances);
  };

  const updateStatus = (id: string, status: string) => {
    // BUG: directly mutating the object inside the array
    const instance = instances.find(i => i.id === id);
    if (instance) {
      instance.status = status;
      setInstances(instances); // same array reference — React skips re-render
    }
  };

  const removeInstance = (id: string) => {
    // BUG: splice mutates the original array
    const index = instances.findIndex(i => i.id === id);
    instances.splice(index, 1);
    setInstances(instances);
  };

  const updateNested = (id: string, key: string, value: string) => {
    // BUG: deep mutation — metadata object is still the same reference
    const instance = instances.find(i => i.id === id);
    if (instance) {
      instance.metadata[key] = value;
      setInstances([...instances]); // spread at top level doesn't help — objects inside are still mutated
    }
  };

  return <InstanceTable instances={instances} />;
}
```

**Correct (immutable updates -- new references at every level that changed):**

```tsx
function InstanceManager() {
  const [instances, setInstances] = useState<Instance[]>([]);

  const addInstance = (newInstance: Instance) => {
    // New array with the new item appended
    setInstances(prev => [...prev, newInstance]);
  };

  const updateStatus = (id: string, status: string) => {
    // New array, new object for the changed item
    setInstances(prev =>
      prev.map(instance =>
        instance.id === id ? { ...instance, status } : instance
      ),
    );
  };

  const removeInstance = (id: string) => {
    // New array without the removed item
    setInstances(prev => prev.filter(instance => instance.id !== id));
  };

  const updateNested = (id: string, key: string, value: string) => {
    // New array, new object, new nested object — immutable at every level
    setInstances(prev =>
      prev.map(instance =>
        instance.id === id
          ? { ...instance, metadata: { ...instance.metadata, [key]: value } }
          : instance
      ),
    );
  };

  return <InstanceTable instances={instances} />;
}
```
