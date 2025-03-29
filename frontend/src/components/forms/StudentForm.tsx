import { TextInput, Select, Button, Stack } from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { Student, studentApi } from '../../lib/api';

interface StudentFormProps {
  student?: Student;
  onSuccess: () => void;
  onCancel: () => void;
}

export function StudentForm({ student, onSuccess, onCancel }: StudentFormProps) {
  const form = useForm({
    initialValues: {
      first_name: student?.first_name || '',
      last_name: student?.last_name || '',
      email: student?.email || '',
      phone: student?.phone || '',
      status: student?.status || 'active',
    },
    validate: {
      first_name: (value) => (!value ? 'First name is required' : null),
      last_name: (value) => (!value ? 'Last name is required' : null),
      email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
      phone: (value) => (!value ? 'Phone number is required' : null),
      status: (value) => (!value ? 'Status is required' : null),
    },
  });

  const handleSubmit = async (values: typeof form.values) => {
    try {
      if (student) {
        await studentApi.update(student.id, values);
        notifications.show({
          title: 'Success',
          message: 'Student updated successfully',
          color: 'green',
        });
      } else {
        await studentApi.create(values);
        notifications.show({
          title: 'Success',
          message: 'Student created successfully',
          color: 'green',
        });
      }
      onSuccess();
    } catch (error) {
      notifications.show({
        title: 'Error',
        message: 'Failed to save student',
        color: 'red',
      });
    }
  };

  return (
    <form onSubmit={form.onSubmit(handleSubmit)}>
      <Stack>
        <TextInput
          label="First Name"
          placeholder="Enter first name"
          required
          {...form.getInputProps('first_name')}
        />
        <TextInput
          label="Last Name"
          placeholder="Enter last name"
          required
          {...form.getInputProps('last_name')}
        />
        <TextInput
          label="Email"
          placeholder="Enter email"
          required
          {...form.getInputProps('email')}
        />
        <TextInput
          label="Phone"
          placeholder="Enter phone number"
          required
          {...form.getInputProps('phone')}
        />
        <Select
          label="Status"
          data={[
            { value: 'active', label: 'Active' },
            { value: 'inactive', label: 'Inactive' },
          ]}
          required
          {...form.getInputProps('status')}
        />
        <Button.Group>
          <Button type="submit">{student ? 'Update' : 'Create'}</Button>
          <Button variant="light" onClick={onCancel}>Cancel</Button>
        </Button.Group>
      </Stack>
    </form>
  );
} 