import { Box, Typography, CircularProgress, Alert } from '@mui/material'
import StatsCards from '../features/dashboard/components/StatsCards'
import DashboardCharts from '../features/dashboard/components/DashboardCharts'
import { useDashboardStats } from '../features/dashboard/hooks/useDashboardStats'

export default function DashboardPage() {
  const { data, isLoading, error } = useDashboardStats()

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Дашборд
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Ключевые метрики и динамика взаимодействий с вузами
      </Typography>

      {isLoading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 6 }}>
          <CircularProgress />
        </Box>
      )}

      {error && <Alert severity="error">Не удалось загрузить данные</Alert>}

      {data && (
        <>
          <StatsCards
            totalUniversities={data.totalUniversities}
            activeWorkflows={data.activeWorkflows}
            completedWorkflows={data.completedWorkflows}
            overdueStages={data.overdueStages}
          />
          <Box sx={{ mt: 3 }}>
            <DashboardCharts
              workflowsByStatus={data.workflowsByStatus}
              workflowsByDirection={data.workflowsByDirection}
              workflowDynamics={data.workflowDynamics}
            />
          </Box>
        </>
      )}
    </Box>
  )
}
