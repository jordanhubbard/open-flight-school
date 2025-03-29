import { Title, Text, Button, Group, Paper, Stack, Badge } from '@mantine/core';
import { IconPlus } from '@tabler/icons-react';

export function Schedule() {
  return (
    <div>
      <Group justify="space-between" mb="xl">
        <div>
          <Title order={2}>Schedule</Title>
          <Text c="dimmed">Manage flight lessons and bookings</Text>
        </div>
        <Button leftSection={<IconPlus size={14} />}>New Booking</Button>
      </Group>

      <Stack>
        <Paper withBorder p="md">
          <Group justify="space-between" mb="xs">
            <div>
              <Title order={4}>John Doe - Cessna 172</Title>
              <Text size="sm" c="dimmed">March 29, 2024 - 10:00 AM</Text>
            </div>
            <Badge color="blue">Scheduled</Badge>
          </Group>
          <Text size="sm">Duration: 1 hour</Text>
          <Group mt="md">
            <Button variant="light" size="xs">Edit</Button>
            <Button variant="light" color="red" size="xs">Cancel</Button>
          </Group>
        </Paper>
      </Stack>
    </div>
  );
} 