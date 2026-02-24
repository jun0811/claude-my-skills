---
title: Place State Closest to Where It's Used
impact: MEDIUM-HIGH
tags: state, colocation, performance
---

## Place State Closest to Where It's Used

Don't lift state higher than necessary. If only one component needs a piece of state, keep it local. Pushing state to global stores or parent components causes unnecessary re-renders across the tree and makes it harder to understand which components own which data.

**Incorrect (global atom for state that only one component uses):**

```tsx
// recoil/atoms/instanceAtoms.ts
// This modal state is used by ONLY the InstanceActions component
export const deleteModalVisibleAtom = atom<boolean>({
  key: 'deleteModalVisible',
  default: false,
});

export const deleteTargetAtom = atom<Instance | null>({
  key: 'deleteTarget',
  default: null,
});

// InstanceActions.tsx — the ONLY consumer
function InstanceActions({ instance }: { instance: Instance }) {
  // Every component subscribed to these atoms re-renders when modal opens
  const [visible, setVisible] = useRecoilState(deleteModalVisibleAtom);
  const [target, setTarget] = useRecoilState(deleteTargetAtom);

  const handleDelete = () => {
    setTarget(instance);
    setVisible(true);
  };

  return (
    <>
      <Button danger onClick={handleDelete}>Delete</Button>
      <DeleteConfirmModal
        visible={visible}
        instance={target}
        onClose={() => setVisible(false)}
      />
    </>
  );
}
```

**Correct (local state in the only component that needs it):**

```tsx
// No global atoms needed — state lives where it's used
function InstanceActions({ instance }: { instance: Instance }) {
  const [deleteModalVisible, setDeleteModalVisible] = useState(false);

  return (
    <>
      <Button danger onClick={() => setDeleteModalVisible(true)}>Delete</Button>
      <DeleteConfirmModal
        visible={deleteModalVisible}
        instance={instance}
        onClose={() => setDeleteModalVisible(false)}
      />
    </>
  );
}

// Reserve global state (Recoil/Zustand) for truly shared data:
// - Current user/auth token (used across many components)
// - Active project/zone selection (affects API calls everywhere)
// - Theme/locale preferences (app-wide)
export const currentProjectAtom = atom<Project>({
  key: 'currentProject',
  default: null,
});
```
