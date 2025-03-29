import { TextInput, NumberInput, Select, Button, Stack, Textarea } from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { Booking, bookingApi, aircraftApi, studentApi } from '../../lib/api';
import { useEffect, useState } from 'react';

interface BookingFormProps {
  booking?: Booking;
  onSuccess: () => void;
  onCancel: () => void;
}

export function BookingForm({ booking, onSuccess, onCancel }: BookingFormProps) {
  const [aircraft, setAircraft] = useState<any[]>([]);
  const [students, setStudents] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [aircraftResponse, studentsResponse] = await Promise.all([
          aircraftApi.getAll(),
          studentApi.getAll(),
        ]);
        setAircraft(aircraftResponse.data);
        setStudents(studentsResponse.data);
      } catch (error) {
        notifications.show({
          title: 'Error',
          message: 'Failed to load aircraft and students',
          color: 'red',
        });
      }
    };
    fetchData();
  }, []);

  const form = useForm({
    initialValues: {
      student_id: booking?.student_id || '',
      aircraft_id: booking?.aircraft_id || '',
      instructor_id: booking?.instructor_id || '',
      start_time: booking?.start_time ? new Date(booking.start_time).toISOString().slice(0, 16) : '',
      duration: booking?.duration || 60,
      status: booking?.status || 'scheduled',
      notes: booking?.notes || '',
    },
    validate: {
      student_id: (value) => (!value ? 'Student is required' : null),
      aircraft_id: (value) => (!value ? 'Aircraft is required' : null),
      instructor_id: (value) => (!value ? 'Instructor is required' : null),
      start_time: (value) => (!value ? 'Start time is required' : null),
      duration: (value) => (!value || value < 30 ? 'Duration must be at least 30 minutes' : null),
      status: (value) => (!value ? 'Status is required' : null),
    },
  });

  const handleSubmit = async (values: typeof form.values) => {
    try {
      if (booking) {
        await bookingApi.update(booking.id, values);
        notifications.show({
          title: 'Success',
          message: 'Booking updated successfully',
          color: 'green',
        });
      } else {
        await bookingApi.create(values);
        notifications.show({
          title: 'Success',
          message: 'Booking created successfully',
          color: 'green',
        });
      }
      onSuccess();
    } catch (error) {
      notifications.show({
        title: 'Error',
        message: 'Failed to save booking',
        color: 'red',
      });
    }
  };

  return (
    <form onSubmit={form.onSubmit(handleSubmit)}>
      <Stack>
        <Select
          label="Student"
          placeholder="Select student"
          data={students.map((s) => ({ value: s.id.toString(), label: `${s.first_name} ${s.last_name}` }))}
          required
          {...form.getInputProps('student_id')}
        />
        <Select
          label="Aircraft"
          placeholder="Select aircraft"
          data={aircraft.map((a) => ({ value: a.id.toString(), label: `${a.type} ${a.model} (${a.registration})` }))}
          required
          {...form.getInputProps('aircraft_id')}
        />
        <Select
          label="Instructor"
          placeholder="Select instructor"
          data={[]} // TODO: Add instructor data
          required
          {...form.getInputProps('instructor_id')}
        />
        <TextInput
          label="Start Time"
          type="datetime-local"
          required
          {...form.getInputProps('start_time')}
        />
        <NumberInput
          label="Duration (minutes)"
          min={30}
          max={480}
          step={30}
          required
          {...form.getInputProps('duration')}
        />
        <Select
          label="Status"
          data={[
            { value: 'scheduled', label: 'Scheduled' },
            { value: 'completed', label: 'Completed' },
            { value: 'cancelled', label: 'Cancelled' },
          ]}
          required
          {...form.getInputProps('status')}
        />
        <Textarea
          label="Notes"
          placeholder="Enter any additional notes"
          {...form.getInputProps('notes')}
        />
        <Button.Group>
          <Button type="submit">{booking ? 'Update' : 'Create'}</Button>
          <Button variant="light" onClick={onCancel}>Cancel</Button>
        </Button.Group>
      </Stack>
    </form>
  );
} 