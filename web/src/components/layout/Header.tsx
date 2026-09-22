import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Menu,
  MenuItem,
  Avatar,
  Chip,
} from '@mui/material'

import MenuIcon from '@mui/icons-material/Menu'
import LogoutIcon from '@mui/icons-material/Logout'
import AccountCircleIcon from '@mui/icons-material/AccountCircle'

import { useState } from 'react'
import { useUserStore } from '../../store/userStore'
import { useUIStore } from '../../store/uiStore'
import { DRAWER_WIDTH } from './Sidebar'

const roleLabels: Record<string, string> = {
  user: 'Пользователь',
  manager: 'Руководитель',
  admin: 'Администратор',
}

export default function Header() {
  const user = useUserStore((s) => s.user)
  const logout = useUserStore((s) => s.logout)
  const toggleSidebar = useUIStore((s) => s.toggleSidebar)

  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const open = Boolean(anchorEl)

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }
  const handleClose = () => setAnchorEl(null)

  return (
    <AppBar
      position="fixed"
      color="inherit"
      elevation={0}
      sx={{
        width: `calc(100% - ${DRAWER_WIDTH}px)`,
        ml: `${DRAWER_WIDTH}px`,
        borderBottom: '1px solid',
        borderColor: 'divider',
      }}
    >
      <Toolbar>
        <IconButton edge="start" onClick={toggleSidebar} sx={{ mr: 2 }}>
          <MenuIcon />
        </IconButton>

        <Box sx={{ flexGrow: 1 }} />

        {user && (
          <Chip
            label={roleLabels[user.role] ?? user.role}
            size="small"
            color="primary"
            variant="outlined"
            sx={{ mr: 2 }}
          />
        )}

        <IconButton onClick={handleMenu} size="small">
          <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
            <AccountCircleIcon />
          </Avatar>
        </IconButton>

        <Menu
          anchorEl={anchorEl}
          open={open}
          onClose={handleClose}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
          transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        >
          <MenuItem disabled>
            <Typography variant="body2">
              {user?.fio ?? 'Пользователь'}
            </Typography>
          </MenuItem>
          <MenuItem disabled>
            <Typography variant="caption" color="text.secondary">
              {user?.email ?? '—'}
            </Typography>
          </MenuItem>
          <MenuItem onClick={() => { handleClose(); logout() }}>
            <LogoutIcon fontSize="small" sx={{ mr: 1 }} />
            Выйти
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  )
}
