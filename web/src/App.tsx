import { Container, Typography, Box, Paper, Stack } from '@mui/material'

function App() {
  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 6 }}>
        <Stack spacing={2} sx={{ alignItems: 'center', textAlign: 'center' }}>
          <Typography variant="h1" sx={{ color: 'primary.main', fontWeight: 700 }}>
            ИТ Школа РТК
          </Typography>
          <Typography variant="h5" color="text.secondary">
            Система контроля и обработки статистических данных
          </Typography>
          <Paper sx={{ p: 4, mt: 4, width: '100%', maxWidth: 600 }}>
            <Typography variant="body1">
              Здесь будет интерфейс CRM: дашборд, каталоги, workflow, отчёты.
            </Typography>
          </Paper>
        </Stack>
      </Box>
    </Container>
  )
}

export default App
