import { Outlet } from 'react-router-dom'
import { Box, Toolbar } from '@mui/material'

import Sidebar, { DRAWER_WIDTH } from './Sidebar'
import Header from './Header'

export default function AppLayout() {
  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          width: `calc(100% - ${DRAWER_WIDTH}px)`,
          bgcolor: 'background.default',
        }}
      >
        <Header />
        <Toolbar /> {/* отступ под AppBar */}
        <Box sx={{ p: 3 }}>
          <Outlet />
        </Box>
      </Box>
    </Box>
  )
}
