import { useState } from 'react'
import { Box, Typography, Snackbar, Alert } from '@mui/material'
import { useQuery, useQueryClient } from '@tanstack/react-query'

import ReportFiltersPanel from '../features/reports/components/ReportFiltersPanel'
import ReportHistory from '../features/reports/components/ReportHistory'
import { reportsApi } from '../api/reports'
import type { ReportColumn, ReportFilters, ReportFormat } from '../api/reports'

export default function ReportsPage() {
  const queryClient = useQueryClient()
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)

  const { data: history = [] } = useQuery({
    queryKey: ['report-history'],
    queryFn: () => reportsApi.getReportHistory(),
  })

  const handleGenerate = async (
    filters: ReportFilters,
    columns: ReportColumn[],
    format: ReportFormat,
  ) => {
    setLoading(true)
    try {
      await reportsApi.generateReport(filters, columns, format)
      await queryClient.invalidateQueries({ queryKey: ['report-history'] })
      setSuccess(true)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Отчёты
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Формирование выгрузок по взаимодействиям с вузами в форматах xls, xlsx, pdf
      </Typography>

      <ReportFiltersPanel onGenerate={handleGenerate} loading={loading} />

      <Typography variant="h6" sx={{ mt: 4, mb: 2 }}>
        История отчётов
      </Typography>
      <ReportHistory reports={history} />

      <Snackbar
        open={success}
        autoHideDuration={3000}
        onClose={() => setSuccess(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert severity="success" onClose={() => setSuccess(false)}>
          Отчёт успешно сформирован
        </Alert>
      </Snackbar>
    </Box>
  )
}
