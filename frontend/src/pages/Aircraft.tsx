import { Title, Text, Button, Group, Card, SimpleGrid, Modal, Badge } from '@mantine/core';
import { IconPlus } from '@tabler/icons-react';
import { useEffect, useState } from 'react';
import { notifications } from '@mantine/notifications';
import { Aircraft as AircraftType, aircraftApi } from '../lib/api';
import { AircraftForm } from '../components/forms/AircraftForm';

export function Aircraft() {
  const [aircraft, setAircraft] = useState<AircraftType[]>([]);
  const [opened, setOpened] = useState(false);
  const [selectedAircraft, setSelectedAircraft] = useState<AircraftType | undefined>();

  const fetchAircraft = async () => {
    try {
      const response = await aircraftApi.getAll();
      setAircraft(response.data);
    } catch (error) {
      notifications.show({
        title: 'Error',
        message: 'Failed to load aircraft',
        color: 'red',
      });
    }
  };

  useEffect(() => {
    fetchAircraft();
  }, []);

  const handleDelete = async (id: number) => {
    try {
      await aircraftApi.delete(id);
      notifications.show({
        title: 'Success',
        message: 'Aircraft deleted successfully',
        color: 'green',
      });
      fetchAircraft();
    } catch (error) {
      notifications.show({
        title: 'Error',
        message: 'Failed to delete aircraft',
        color: 'red',
      });
    }
  };

  const handleEdit = (aircraft: AircraftType) => {
    setSelectedAircraft(aircraft);
    setOpened(true);
  };

  const handleCreate = () => {
    setSelectedAircraft(undefined);
    setOpened(true);
  };

  const handleFormSuccess = () => {
    setOpened(false);
    fetchAircraft();
  };

  return (
    <div>
      <Group justify="space-between" mb="xl">
        <div>
          <Title order={2}>Aircraft Fleet</Title>
          <Text c="dimmed">Manage your aircraft inventory</Text>
        </div>
        <Button leftSection={<IconPlus size={14} />} onClick={handleCreate}>
          Add Aircraft
        </Button>
      </Group>

      <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }}>
        {aircraft.map((item) => (
          <Card key={item.id} withBorder>
            <Title order={3}>{item.type} {item.model}</Title>
            <Text size="sm" c="dimmed">Registration: {item.registration}</Text>
            <Text size="sm" c="dimmed">Total Hours: {item.total_hours}</Text>
            <Text size="sm" c="dimmed">Last Maintenance: {new Date(item.last_maintenance).toLocaleDateString()}</Text>
            <Badge
              color={
                item.status === 'available'
                  ? 'green'
                  : item.status === 'maintenance'
                  ? 'yellow'
                  : 'blue'
              }
              mb="md"
            >
              {item.status.charAt(0).toUpperCase() + item.status.slice(1)}
            </Badge>
            <Group mt="md">
              <Button variant="light" size="xs" onClick={() => handleEdit(item)}>
                Edit
              </Button>
              <Button
                variant="light"
                color="red"
                size="xs"
                onClick={() => handleDelete(item.id)}
              >
                Delete
              </Button>
            </Group>
          </Card>
        ))}
      </SimpleGrid>

      <Modal
        opened={opened}
        onClose={() => setOpened(false)}
        title={selectedAircraft ? 'Edit Aircraft' : 'Add Aircraft'}
        size="md"
      >
        <AircraftForm
          aircraft={selectedAircraft}
          onSuccess={handleFormSuccess}
          onCancel={() => setOpened(false)}
        />
      </Modal>
    </div>
  );
} 