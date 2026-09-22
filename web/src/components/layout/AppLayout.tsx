import { Outlet } from 'react-router-dom'
import { Box } from '@mui/material'

export default function AppLayout() {
  return (
    <Box>
      <Outlet />
    </Box>
  )
}
