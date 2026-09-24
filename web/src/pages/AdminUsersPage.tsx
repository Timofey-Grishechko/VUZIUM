import { Box, Typography, CircularProgress } from '@mui/material'
import UsersTable from '../features/admin/components/UsersTable'
import { useUsers } from '../features/admin/hooks/useUsers'

export default function AdminUsersPage() {
  const { data: users = [], isLoading } = useUsers()

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Пользователи
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Управление ролями и доступом пользователей к данным системы
      </Typography>

      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 6 }}>
          <CircularProgress />
        </Box>
      ) : (
        <UsersTable users={users} />
      )}
    </Box>
  )
}
