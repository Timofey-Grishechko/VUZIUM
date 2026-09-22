import { Box } from '@mui/material'
import LoginCard from '../features/auth/components/LoginCard'

export default function LoginPage() {
  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        p: 2,
        background: (theme) =>
          `linear-gradient(135deg, ${theme.palette.primary.light}22 0%, ${theme.palette.primary.main}33 100%)`,
      }}
    >
      <LoginCard />
    </Box>
  )
}
