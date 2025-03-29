import { TextInput, NumberInput, Select, Button, Stack } from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { Aircraft, aircraftApi } from '../../lib/api';

interface AircraftFormProps {
  aircraft?: Aircraft;
  onSuccess: () => void;
  onCancel: () => void;
}

export function AircraftForm({ aircraft, onSuccess, onCancel }: AircraftFormProps) {
  const form = useForm({
    initialValues: {
      type: aircraft?.type || '',
      model: aircraft?.model || '',
      registration: aircraft?.registration || '',
      status: aircraft?.status || 'active',
      total_hours: aircraft?.total_hours || 0,
      last_maintenance: aircraft?.last_maintenance || '',
    },
    validate: {
      type: (value) => (!value ? 'Type is required' : null),
      model: (value) => (!value ? 'Model is required' : null),
      registration: (value) => (!value ? 'Registration is required' : null),
      status: (value) => (!value ? 'Status is required' : null),
      total_hours: (value) => (value < 0 ? 'Total hours cannot be negative' : null),
      last_maintenance: (value) => (!value ? 'Last maintenance date is required' : null),
    },
  });

  const handleSubmit = async (values: typeof form.values) => {
    try {
      if (aircraft) {
        await aircraftApi.update(aircraft.id, values);
        notifications.show({
          title: 'Success',
          message: 'Aircraft updated successfully',
          color: 'green',
        });
      } else {
        await aircraftApi.create(values);
        notifications.show({
          title: 'Success',
          message: 'Aircraft created successfully',
          color: 'green',
        });
      }
      onSuccess();
    } catch (error) {
      notifications.show({
        title: 'Error',
        message: aircraft ? 'Failed to update aircraft' : 'Failed to create aircraft',
        color: 'red',
      });
    }
  };

  return (
    <form onSubmit={form.onSubmit(handleSubmit)}>
      <Stack>
        <TextInput
          label="Type"
          placeholder="Enter aircraft type"
          required
          {...form.getInputProps('type')}
        />
        <TextInput
          label="Model"
          placeholder="Enter aircraft model"
          required
          {...form.getInputProps('model')}
        />
        <TextInput
          label="Registration"
          placeholder="Enter aircraft registration"
          required
          {...form.getInputProps('registration')}
        />
        <Select
          label="Status"
          placeholder="Select status"
          required
          data={[
            { value: 'active', label: 'Active' },
            { value: 'maintenance', label: 'Maintenance' },
            { value: 'inactive', label: 'Inactive' },
          ]}
          {...form.getInputProps('status')}
        />
        <NumberInput
          label="Total Hours"
          placeholder="Enter total hours"
          required
          min={0}
          {...form.getInputProps('total_hours')}
        />
        <TextInput
          label="Last Maintenance"
          placeholder="YYYY-MM-DD"
          required
          {...form.getInputProps('last_maintenance')}
        />
        <Button type="submit">
          {aircraft ? 'Update Aircraft' : 'Create Aircraft'}
        </Button>
        <Button variant="light" onClick={onCancel}>
          Cancel
        </Button>
      </Stack>
    </form>
  );
} 