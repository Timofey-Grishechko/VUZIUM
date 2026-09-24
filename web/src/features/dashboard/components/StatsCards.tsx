import { Grid, Card, CardContent, Typography, Box } from '@mui/material'
import SchoolIcon from '@mui/icons-material/School'
import AccountTreeIcon from '@mui/icons-material/AccountTree'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import WarningIcon from '@mui/icons-material/Warning'

interface Props {
  totalUniversities: number
  activeWorkflows: number
  completedWorkflows: number
  overdueStages: number
}

const cards = [
  { key: 'totalUniversities', label: 'Вузов в системе', icon: SchoolIcon, color: '#6A1B9A' },
  { key: 'activeWorkflows', label: 'Активных workflow', icon: AccountTreeIcon, color: '#00897B' },
  { key: 'completedWorkflows', label: 'Завершено', icon: CheckCircleIcon, color: '#43A047' },
  { key: 'overdueStages', label: 'Требуют внимания', icon: WarningIcon, color: '#E53935' },
] as const

export default function StatsCards(props: Props) {
  return (
    <Grid container spacing={2} sx={{ alignItems: 'stretch' }}>
      {cards.map((c) => {
        const Icon = c.icon
        const value = props[c.key]
        return (
          <Grid key={c.key} size={{ xs: 12, sm: 6, md: 3 }}>
            <Card
              elevation={0}
              sx={{
                height: '100%',
                border: '1px solid',
                borderColor: 'divider',
              }}
            >
              <CardContent sx={{ height: '100%' }}>
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    height: '100%',
                    gap: 2,
                  }}
                >
                  <Box sx={{ minWidth: 0, flexGrow: 1 }}>
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      sx={{
                        mb: 1,
                        minHeight: 40,        // ← фиксируем высоту под 2 строки
                        lineHeight: 1.3,
                        display: 'flex',
                        alignItems: 'center',
                      }}
                    >
                      {c.label}
                    </Typography>
                    <Typography
                      variant="h4"
                      sx={{ fontWeight: 700, lineHeight: 1 }}
                    >
                      {value}
                    </Typography>
                  </Box>

                  <Box
                    sx={{
                      width: 44,
                      height: 44,
                      borderRadius: 2,
                      bgcolor: `${c.color}15`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: c.color,
                      flexShrink: 0,
                    }}
                  >
                    <Icon />
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        )
      })}
    </Grid>
  )
}
