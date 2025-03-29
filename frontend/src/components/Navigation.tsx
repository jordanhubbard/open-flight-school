import { NavLink, Stack } from '@mantine/core';
import { IconPlane, IconUsers, IconCalendar, IconSettings } from '@tabler/icons-react';
import { Link } from 'react-router-dom';

export function Navigation() {
  return (
    <Stack>
      <NavLink
        label="Aircraft"
        leftSection={<IconPlane size="1.2rem" stroke={1.5} />}
        component={Link}
        to="/aircraft"
      />
      <NavLink
        label="Students"
        leftSection={<IconUsers size="1.2rem" stroke={1.5} />}
        component={Link}
        to="/students"
      />
      <NavLink
        label="Schedule"
        leftSection={<IconCalendar size="1.2rem" stroke={1.5} />}
        component={Link}
        to="/schedule"
      />
      <NavLink
        label="Settings"
        leftSection={<IconSettings size="1.2rem" stroke={1.5} />}
        component={Link}
        to="/settings"
      />
    </Stack>
  );
} 