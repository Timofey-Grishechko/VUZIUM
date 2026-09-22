import { useState } from 'react'
import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Divider,
  MenuItem,
  Stack,
  TextField,
  Typography,
  Alert,
} from '@mui/material'
import LoginIcon from '@mui/icons-material/Login'

import { useAuth } from '../hooks/useAuth'
import type { Role } from '../../../types/user'

const roleOptions: { value: Role; label: string }[] = [
  { value: 'user', label: 'Пользователь (НАМ)' },
  { value: 'manager', label: 'Руководитель' },
  { value: 'admin', label: 'Администратор' },
]

export default function LoginCard() {
  const { login, loading, error } = useAuth()
  const [role, setRole] = useState<Role>('manager')

  const handleLogin = () => {
    void login(role)
  }

  return (
    <Card
      elevation={6}
      sx={{ width: '100%', maxWidth: 440, borderRadius: 3 }}
    >
      <CardContent sx={{ p: 4 }}>
        <Stack spacing={1} sx={{ mb: 3, textAlign: 'center' }}>
          <Typography variant="h4" sx={{ fontWeight: 700, color: 'primary.main' }}>
            VUZIUM
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Система контроля обучения по ИТ-направлениям
          </Typography>
        </Stack>

        <Divider sx={{ mb: 3 }} />

        <Typography variant="h6" gutterBottom>
          Вход в систему
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Авторизация через Keycloak
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Stack spacing={2}>
          <TextField
            select
            label="Демо-роль"
            value={role}
            onChange={(e) => setRole(e.target.value as Role)}
            fullWidth
            helperText="Пока Keycloak не подключён — выберите роль для теста"
          >
            {roleOptions.map((opt) => (
              <MenuItem key={opt.value} value={opt.value}>
                {opt.label}
              </MenuItem>
            ))}
          </TextField>

          <Button
            variant="contained"
            size="large"
            startIcon={
              loading ? <CircularProgress size={18} color="inherit" /> : <LoginIcon />
            }
            disabled={loading}
            onClick={handleLogin}
            sx={{ py: 1.5 }}
          >
            {loading ? 'Вход…' : 'Войти через Keycloak'}
          </Button>
        </Stack>

        <Box sx={{ mt: 3, textAlign: 'center' }}>
          <Typography variant="caption" color="text.secondary">
            VUZIUM © ИТ Школа РТК, {new Date().getFullYear()}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  )
}
