---
title: Split Large Components by Responsibility
impact: CRITICAL
tags: refactoring, components, SRP
---

## Split Large Components by Responsibility

When a component renders multiple distinct sections (header, filters, table, modals), each section should be extracted into its own component. A single component should have one reason to change. This reduces cognitive load and makes each piece independently testable.

**Incorrect (single component handles header, filters, table, and modal -- 200+ lines):**

```tsx
const InstancePage = ({ instances, loading, onDelete, onRefresh }: InstancePageProps) => {
  const [filterForm] = Form.useForm();
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedInstance, setSelectedInstance] = useState<Instance | null>(null);

  return (
    <div className="instance-page">
      {/* Header section */}
      <div className="page-header">
        <h2>Instances</h2>
        <Space>
          <Button onClick={onRefresh}>Refresh</Button>
          <Button type="primary" onClick={() => setModalVisible(true)}>Create</Button>
        </Space>
      </div>

      {/* Filter section */}
      <Form form={filterForm} layout="inline" className="filter-form">
        <Form.Item name="status" label="Status">
          <Select options={STATUS_OPTIONS} allowClear />
        </Form.Item>
        <Form.Item name="name" label="Name">
          <Input.Search placeholder="Search by name" />
        </Form.Item>
        <Form.Item>
          <Button onClick={() => filterForm.resetFields()}>Reset</Button>
        </Form.Item>
      </Form>

      {/* Table section */}
      <Table
        dataSource={instances}
        loading={loading}
        columns={[
          { title: 'Name', dataIndex: 'name', sorter: (a, b) => a.name.localeCompare(b.name) },
          { title: 'Status', dataIndex: 'status', render: (s) => <Tag color={STATUS_COLOR[s]}>{s}</Tag> },
          { title: 'IP', dataIndex: 'ip' },
          {
            title: 'Actions',
            render: (_, record) => (
              <Space>
                <Button size="small" onClick={() => setSelectedInstance(record)}>Detail</Button>
                <Popconfirm title="Delete?" onConfirm={() => onDelete(record.id)}>
                  <Button size="small" danger>Delete</Button>
                </Popconfirm>
              </Space>
            ),
          },
        ]}
      />

      {/* Modal section */}
      <Modal title="Create Instance" open={modalVisible} onCancel={() => setModalVisible(false)}>
        {/* ... 50 more lines of form fields */}
      </Modal>
    </div>
  );
};
```

**Correct (each section is its own focused component):**

```tsx
// PageToolbar.tsx
interface PageToolbarProps {
  onRefresh: () => void;
  onCreate: () => void;
}

const PageToolbar = ({ onRefresh, onCreate }: PageToolbarProps) => (
  <div className="page-header">
    <h2>Instances</h2>
    <Space>
      <Button onClick={onRefresh}>Refresh</Button>
      <Button type="primary" onClick={onCreate}>Create</Button>
    </Space>
  </div>
);

// InstanceFilter.tsx
interface InstanceFilterProps {
  onFilter: (values: FilterValues) => void;
  onReset: () => void;
}

const InstanceFilter = ({ onFilter, onReset }: InstanceFilterProps) => {
  const [form] = Form.useForm();
  return (
    <Form form={form} layout="inline" onFinish={onFilter}>
      <Form.Item name="status" label="Status">
        <Select options={STATUS_OPTIONS} allowClear />
      </Form.Item>
      <Form.Item name="name" label="Name">
        <Input.Search placeholder="Search by name" />
      </Form.Item>
      <Form.Item>
        <Button onClick={() => { form.resetFields(); onReset(); }}>Reset</Button>
      </Form.Item>
    </Form>
  );
};

// InstanceTable.tsx
interface InstanceTableProps {
  instances: Instance[];
  loading: boolean;
  onSelect: (instance: Instance) => void;
  onDelete: (id: string) => void;
}

const InstanceTable = ({ instances, loading, onSelect, onDelete }: InstanceTableProps) => (
  <Table dataSource={instances} loading={loading} columns={buildColumns({ onSelect, onDelete })} />
);

// InstancePage.tsx — orchestrator, thin and scannable
const InstancePage = (props: InstancePageProps) => {
  const [modalVisible, setModalVisible] = useState(false);

  return (
    <div className="instance-page">
      <PageToolbar onRefresh={props.onRefresh} onCreate={() => setModalVisible(true)} />
      <InstanceFilter onFilter={props.onFilter} onReset={props.onResetFilter} />
      <InstanceTable
        instances={props.instances}
        loading={props.loading}
        onSelect={props.onSelectInstance}
        onDelete={props.onDelete}
      />
      <CreateInstanceModal open={modalVisible} onClose={() => setModalVisible(false)} />
    </div>
  );
};
```
