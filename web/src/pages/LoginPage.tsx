import { Container, Typography, Box } from '@mui/material'

export default function LoginPage() {
  return (
    <Container maxWidth="sm">
      <Box sx={{ py: 8, textAlign: 'center' }}>
        <Typography variant="h4" gutterBottom>
          Вход в систему
        </Typography>
        <Typography color="text.secondary">
          Здесь будет кнопка входа через Keycloak
        </Typography>
      </Box>
    </Container>
  )
}
