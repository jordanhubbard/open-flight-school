import { Title, Text, Button, Group, Paper, Stack, TextInput, Switch, NumberInput } from '@mantine/core';

export function Settings() {
  return (
    <div>
      <Title order={2} mb="xl">Settings</Title>

      <Stack>
        <Paper withBorder p="md">
          <Title order={4} mb="md">School Information</Title>
          <Stack>
            <TextInput
              label="School Name"
              placeholder="Enter school name"
              defaultValue="Open Flight School"
            />
            <TextInput
              label="Email"
              placeholder="Enter email"
              defaultValue="contact@openflightschool.com"
            />
            <TextInput
              label="Phone"
              placeholder="Enter phone number"
              defaultValue="(555) 123-4567"
            />
            <TextInput
              label="Address"
              placeholder="Enter address"
              defaultValue="123 Aviation Way, Airport City, ST 12345"
            />
          </Stack>
        </Paper>

        <Paper withBorder p="md">
          <Title order={4} mb="md">Preferences</Title>
          <Stack>
            <Switch
              label="Enable email notifications"
              defaultChecked
            />
            <Switch
              label="Enable SMS notifications"
              defaultChecked
            />
            <NumberInput
              label="Default lesson duration (minutes)"
              defaultValue={60}
              min={30}
              max={480}
              step={30}
            />
          </Stack>
        </Paper>

        <Group justify="flex-end">
          <Button variant="light">Cancel</Button>
          <Button>Save Changes</Button>
        </Group>
      </Stack>
    </div>
  );
} 