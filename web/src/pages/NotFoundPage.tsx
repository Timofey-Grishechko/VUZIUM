import { Container, Typography, Box, Button } from '@mui/material'
import { Link } from 'react-router-dom'

export default function NotFoundPage() {
  return (
    <Container maxWidth="sm">
      <Box sx={{ py: 10, textAlign: 'center' }}>
        <Typography variant="h3" gutterBottom>
          404
        </Typography>
        <Typography variant="h6" gutterBottom color="text.secondary">
          Страница не найдена
        </Typography>
        <Button component={Link} to="/" variant="contained" sx={{ mt: 3 }}>
          На главную
        </Button>
      </Box>
    </Container>
  )
}
