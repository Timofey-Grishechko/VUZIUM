import {
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Divider,
  Box,
  Typography,
  useMediaQuery,
  useTheme,
} from '@mui/material'

import DashboardIcon from '@mui/icons-material/Dashboard'
import SchoolIcon from '@mui/icons-material/School'
import CategoryIcon from '@mui/icons-material/Category'
import Inventory2Icon from '@mui/icons-material/Inventory2'
import AccountTreeIcon from '@mui/icons-material/AccountTree'
import AssessmentIcon from '@mui/icons-material/Assessment'
import UploadFileIcon from '@mui/icons-material/UploadFile'
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings'
import HelpOutlineIcon from '@mui/icons-material/HelpOutlined'

import { NavLink, useLocation } from 'react-router-dom'
import { useUIStore } from '../../store/uiStore'
import { useUserStore } from '../../store/userStore'

const DRAWER_WIDTH = 260

const mainItems = [
  { to: '/', label: 'Дашборд', icon: <DashboardIcon /> },
  { to: '/universities', label: 'Вузы', icon: <SchoolIcon /> },
  { to: '/directions', label: 'ИТ-направления', icon: <CategoryIcon /> },
  { to: '/products', label: 'ИТ-продукты', icon: <Inventory2Icon /> },
  { to: '/workflows', label: 'Workflow', icon: <AccountTreeIcon /> },
  { to: '/reports', label: 'Отчёты', icon: <AssessmentIcon /> },
]

const adminItems = [
  { to: '/imports', label: 'Импорт данных', icon: <UploadFileIcon /> },
  { to: '/admin/users', label: 'Пользователи', icon: <AdminPanelSettingsIcon /> },
]

const footerItems = [
  { to: '/help', label: 'Помощь', icon: <HelpOutlineIcon /> },
]

export default function Sidebar() {
  const hasRole = useUserStore((s) => s.hasRole)
  const location = useLocation()
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))

  const mobileOpen = useUIStore((s) => s.mobileOpen)
  const closeMobile = useUIStore((s) => s.closeMobile)

  const isActive = (to: string) =>
    to === '/' ? location.pathname === '/' : location.pathname.startsWith(to)

  const handleItemClick = () => {
    if (isMobile) closeMobile()
  }

  const drawerContent = (
    <>
      <Toolbar sx={{ px: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 700, color: 'primary.main' }}>
          VUZIUM
        </Typography>
      </Toolbar>
      <Divider />

      <Box sx={{ overflowY: 'auto', flexGrow: 1 }}>
        <List>
          {mainItems.map((item) => (
            <ListItemButton
              key={item.to}
              component={NavLink}
              to={item.to}
              selected={isActive(item.to)}
              onClick={handleItemClick}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.label} />
            </ListItemButton>
          ))}
        </List>

        {hasRole(['manager', 'admin']) && (
          <>
            <Divider />
            <List>
              {adminItems.map((item) => (
                <ListItemButton
                  key={item.to}
                  component={NavLink}
                  to={item.to}
                  selected={isActive(item.to)}
                  onClick={handleItemClick}
                >
                  <ListItemIcon>{item.icon}</ListItemIcon>
                  <ListItemText primary={item.label} />
                </ListItemButton>
              ))}
            </List>
          </>
        )}

        <Divider />
        <List>
          {footerItems.map((item) => (
            <ListItemButton
              key={item.to}
              component={NavLink}
              to={item.to}
              selected={isActive(item.to)}
              onClick={handleItemClick}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.label} />
            </ListItemButton>
          ))}
        </List>
      </Box>
    </>
  )

  // На мобилке — temporary Drawer (выезжает по бургеру)
  if (isMobile) {
    return (
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={closeMobile}
        ModalProps={{ keepMounted: true }}
        sx={{
          '& .MuiDrawer-paper': {
            width: DRAWER_WIDTH,
            boxSizing: 'border-box',
          },
        }}
      >
        {drawerContent}
      </Drawer>
    )
  }

  // На десктопе — permanent Drawer (всегда слева)
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: DRAWER_WIDTH,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: DRAWER_WIDTH,
          boxSizing: 'border-box',
          borderRight: '1px solid',
          borderColor: 'divider',
        },
      }}
      open
    >
      {drawerContent}
    </Drawer>
  )
}

export { DRAWER_WIDTH }
