import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Switch,
  MenuItem,
  TextField,
  Box,
} from '@mui/material'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { adminApi } from '../../../api/admin'
import type { Role, User } from '../../../types/user'

interface Props {
  users: User[]
}

const roleColors: Record<Role, 'default' | 'primary' | 'secondary'> = {
  user: 'default',
  manager: 'primary',
  admin: 'secondary',
}

const roleLabels: Record<Role, string> = {
  user: 'Пользователь',
  manager: 'Руководитель',
  admin: 'Администратор',
}

export default function UsersTable({ users }: Props) {
  const queryClient = useQueryClient()

  const roleMutation = useMutation({
    mutationFn: ({ userId, role }: { userId: string; role: Role }) =>
      adminApi.updateUserRole(userId, role),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin-users'] }),
  })

  const activeMutation = useMutation({
    mutationFn: (userId: string) => adminApi.toggleUserActive(userId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin-users'] }),
  })

  return (
    <Paper elevation={0} sx={{ border: '1px solid', borderColor: 'divider' }}>
      <TableContainer>
        <Table sx={{ minWidth: 700 }}>
          <TableHead>
            <TableRow>
              <TableCell>ФИО</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Роль</TableCell>
              <TableCell>Вузы</TableCell>
              <TableCell align="center">Активен</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((u) => (
              <TableRow key={u.id} hover>
                <TableCell>{u.fio}</TableCell>
                <TableCell>{u.email}</TableCell>
                <TableCell>
                  <TextField
                    select
                    size="small"
                    value={u.role}
                    onChange={(e) =>
                      roleMutation.mutate({ userId: u.id, role: e.target.value as Role })
                    }
                    sx={{ minWidth: 160 }}
                  >
                    <MenuItem value="user">Пользователь</MenuItem>
                    <MenuItem value="manager">Руководитель</MenuItem>
                    <MenuItem value="admin">Администратор</MenuItem>
                  </TextField>
                </TableCell>
                <TableCell>
                  {u.universityIds.length > 0 ? (
                    <Chip
                      label={`${u.universityIds.length} вуз(а)`}
                      size="small"
                      variant="outlined"
                    />
                  ) : (
                    <Chip label="Все" size="small" color="primary" variant="outlined" />
                  )}
                </TableCell>
                <TableCell align="center">
                  <Switch
                    checked={u.active}
                    onChange={() => activeMutation.mutate(u.id)}
                    color="primary"
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  )
}
