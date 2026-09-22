import { Container, Typography, Box } from '@mui/material'

export default function DashboardPage() {
  return (
    <Container>
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" gutterBottom>
          Дашборд
        </Typography>
        <Typography color="text.secondary">
          Здесь будут счётчики, графики и таблица «требуют внимания»
        </Typography>
      </Box>
    </Container>
  )
}
