import { createTheme } from '@mui/material/styles'

// Цвета РТК (приблизительные, надо будет - поменяю.)
const RTK_PURPLE = '#6A1B9A'
const RTK_VIOLET = '#7B2FBE'

export const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: RTK_PURPLE,
      light: RTK_VIOLET,
    },
    secondary: {
      main: '#00897B',
    },
    background: {
      default: '#F5F5F7',
      paper: '#FFFFFF',
    },
  },
  typography: {
    fontFamily: [
      'Inter',
      'Roboto',
      '-apple-system',
      'BlinkMacSystemFont',
      'Segoe UI',
      'Arial',
      'sans-serif',
    ].join(','),
    h1: { fontSize: '2rem', fontWeight: 600 },
    h2: { fontSize: '1.5rem', fontWeight: 600 },
    h3: { fontSize: '1.25rem', fontWeight: 600 },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 500,
        },
      },
    },
  },
})
