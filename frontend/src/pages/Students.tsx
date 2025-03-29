import { Title, Text, Button, Group, Table, Badge, Modal } from '@mantine/core';
import { IconPlus } from '@tabler/icons-react';
import { useEffect, useState } from 'react';
import { notifications } from '@mantine/notifications';
import { Student, studentApi } from '../lib/api';
import { StudentForm } from '../components/forms/StudentForm';

export function Students() {
  const [students, setStudents] = useState<Student[]>([]);
  const [opened, setOpened] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState<Student | undefined>();

  const fetchStudents = async () => {
    try {
      const response = await studentApi.getAll();
      setStudents(response.data);
    } catch (error) {
      notifications.show({
        title: 'Error',
        message: 'Failed to load students',
        color: 'red',
      });
    }
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  const handleDelete = async (id: number) => {
    try {
      await studentApi.delete(id);
      notifications.show({
        title: 'Success',
        message: 'Student deleted successfully',
        color: 'green',
      });
      fetchStudents();
    } catch (error) {
      notifications.show({
        title: 'Error',
        message: 'Failed to delete student',
        color: 'red',
      });
    }
  };

  const handleEdit = (student: Student) => {
    setSelectedStudent(student);
    setOpened(true);
  };

  const handleCreate = () => {
    setSelectedStudent(undefined);
    setOpened(true);
  };

  const handleFormSuccess = () => {
    setOpened(false);
    fetchStudents();
  };

  return (
    <div>
      <Group justify="space-between" mb="xl">
        <div>
          <Title order={2}>Students</Title>
          <Text c="dimmed">Manage your student roster</Text>
        </div>
        <Button leftSection={<IconPlus size={14} />} onClick={handleCreate}>
          Add Student
        </Button>
      </Group>

      <Table>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Name</Table.Th>
            <Table.Th>Email</Table.Th>
            <Table.Th>Phone</Table.Th>
            <Table.Th>Status</Table.Th>
            <Table.Th>Actions</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {students.map((student) => (
            <Table.Tr key={student.id}>
              <Table.Td>{student.first_name} {student.last_name}</Table.Td>
              <Table.Td>{student.email}</Table.Td>
              <Table.Td>{student.phone}</Table.Td>
              <Table.Td>
                <Badge color={student.status === 'active' ? 'green' : 'red'}>
                  {student.status.charAt(0).toUpperCase() + student.status.slice(1)}
                </Badge>
              </Table.Td>
              <Table.Td>
                <Group gap="xs">
                  <Button variant="light" size="xs" onClick={() => handleEdit(student)}>
                    Edit
                  </Button>
                  <Button
                    variant="light"
                    color="red"
                    size="xs"
                    onClick={() => handleDelete(student.id)}
                  >
                    Delete
                  </Button>
                </Group>
              </Table.Td>
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>

      <Modal
        opened={opened}
        onClose={() => setOpened(false)}
        title={selectedStudent ? 'Edit Student' : 'Add Student'}
        size="md"
      >
        <StudentForm
          student={selectedStudent}
          onSuccess={handleFormSuccess}
          onCancel={() => setOpened(false)}
        />
      </Modal>
    </div>
  );
} 