---
title: Compute Derived Values, Don't Store Them
impact: MEDIUM-HIGH
tags: state, derived, computation
---

## Compute Derived Values, Don't Store Them

Values that can be calculated from existing state or props should be computed inline or via useMemo, never stored in separate state. The `useEffect` + `setState` pattern for derived data creates unnecessary render cycles and temporal inconsistency where the derived state is one render behind.

**Incorrect (useEffect to sync derived state -- extra renders, stale data between renders):**

```tsx
function VolumeDetail({ volume }: { volume: Volume }) {
  const [sizeInGB, setSizeInGB] = useState(0);
  const [isLargeVolume, setIsLargeVolume] = useState(false);
  const [formattedDate, setFormattedDate] = useState('');
  const [attachedInstanceNames, setAttachedInstanceNames] = useState<string[]>([]);

  // Anti-pattern: each useEffect causes an extra render
  // Between renders, these values are OUT OF SYNC with the volume prop
  useEffect(() => {
    setSizeInGB(volume.size / 1024);
  }, [volume.size]);

  useEffect(() => {
    setIsLargeVolume(volume.size > 1024 * 100);
  }, [volume.size]);

  useEffect(() => {
    setFormattedDate(dayjs(volume.createdAt).format('YYYY-MM-DD HH:mm'));
  }, [volume.createdAt]);

  useEffect(() => {
    setAttachedInstanceNames(volume.attachments.map(a => a.instanceName));
  }, [volume.attachments]);

  // 4 extra renders just to compute values that could be inline
  return (
    <Descriptions>
      <Descriptions.Item label="Size">{sizeInGB} GB</Descriptions.Item>
      <Descriptions.Item label="Type">
        {isLargeVolume ? <Tag color="red">Large</Tag> : <Tag>Standard</Tag>}
      </Descriptions.Item>
      <Descriptions.Item label="Created">{formattedDate}</Descriptions.Item>
      <Descriptions.Item label="Attached">
        {attachedInstanceNames.join(', ')}
      </Descriptions.Item>
    </Descriptions>
  );
}
```

**Correct (compute directly -- zero extra renders, always consistent):**

```tsx
function VolumeDetail({ volume }: { volume: Volume }) {
  // Simple derivations: compute inline, no useMemo needed
  const sizeInGB = volume.size / 1024;
  const isLargeVolume = volume.size > 1024 * 100;
  const formattedDate = dayjs(volume.createdAt).format('YYYY-MM-DD HH:mm');

  // Slightly more expensive derivation: useMemo if attachments list is large
  const attachedInstanceNames = useMemo(
    () => volume.attachments.map(a => a.instanceName),
    [volume.attachments],
  );

  // No extra renders, no stale intermediate states
  return (
    <Descriptions>
      <Descriptions.Item label="Size">{sizeInGB} GB</Descriptions.Item>
      <Descriptions.Item label="Type">
        {isLargeVolume ? <Tag color="red">Large</Tag> : <Tag>Standard</Tag>}
      </Descriptions.Item>
      <Descriptions.Item label="Created">{formattedDate}</Descriptions.Item>
      <Descriptions.Item label="Attached">
        {attachedInstanceNames.join(', ')}
      </Descriptions.Item>
    </Descriptions>
  );
}
```
