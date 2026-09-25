import { useState } from 'react'
import {
  Box,
  Typography,
  Grid,
  List,
  ListItemButton,
  ListItemText,
  Paper,
  Divider,
} from '@mui/material'
import { helpSections } from '../features/help/content'

export default function HelpPage() {
  const [selectedId, setSelectedId] = useState(helpSections[0].id)
  const selected = helpSections.find((s) => s.id === selectedId) ?? helpSections[0]

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Помощь
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Руководство пользователя и администратора системы VUZIUM
      </Typography>

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 3 }}>
          <Paper elevation={0} sx={{ border: '1px solid', borderColor: 'divider' }}>
            <List dense>
              {helpSections.map((s) => (
                <ListItemButton
                  key={s.id}
                  selected={s.id === selectedId}
                  onClick={() => setSelectedId(s.id)}
                >
                  <ListItemText primary={s.title} />
                </ListItemButton>
              ))}
            </List>
          </Paper>
        </Grid>

        <Grid size={{ xs: 12, md: 9 }}>
          <Paper
            elevation={0}
            sx={{ p: 3, border: '1px solid', borderColor: 'divider' }}
          >
            <Typography variant="h5" gutterBottom>
              {selected.title}
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Box
              sx={{
                '& p': { mb: 1.5, lineHeight: 1.7 },
                '& ul, & ol': { pl: 3, mb: 1.5 },
                '& li': { mb: 0.5, lineHeight: 1.7 },
                '& strong': { color: 'primary.main' },
              }}
            >
              {selected.content}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )
}
