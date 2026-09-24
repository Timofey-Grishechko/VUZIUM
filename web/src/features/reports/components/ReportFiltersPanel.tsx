import {
  Card,
  CardContent,
  Grid,
  TextField,
  MenuItem,
  Typography,
  FormGroup,
  FormControlLabel,
  Checkbox,
  Stack,
  Button,
  CircularProgress,
  Divider,
} from '@mui/material'
import DownloadIcon from '@mui/icons-material/Download'
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'

import { reportsApi, DEFAULT_COLUMNS } from '../../../api/reports'
import type { ReportColumn, ReportFilters, ReportFormat } from '../../../api/reports'

interface Props {
  onGenerate: (
    filters: ReportFilters,
    columns: ReportColumn[],
    format: ReportFormat,
  ) => Promise<void>
  loading: boolean
}

export default function ReportFiltersPanel({ onGenerate, loading }: Props) {
  const [filters, setFilters] = useState<ReportFilters>({})
  const [columns, setColumns] = useState<ReportColumn[]>(DEFAULT_COLUMNS)
  const [format, setFormat] = useState<ReportFormat>('xlsx')

  const { data: options } = useQuery({
    queryKey: ['report-filter-options'],
    queryFn: () => reportsApi.getFilterOptions(),
    staleTime: 60_000,
  })

  const toggleColumn = (key: string) => {
    setColumns((cols) =>
      cols.map((c) => (c.key === key ? { ...c, selected: !c.selected } : c)),
    )
  }

  const handleGenerate = () => {
    void onGenerate(filters, columns.filter((c) => c.selected), format)
  }

  return (
    <Card elevation={0} sx={{ border: '1px solid', borderColor: 'divider' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Параметры отчёта
        </Typography>

        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid size={{ xs: 12, sm: 6 }}>
            <TextField
              label="Период с"
              type="date"
              fullWidth
              size="small"
              slotProps={{ inputLabel: { shrink: true } }}
              value={filters.dateFrom ?? ''}
              onChange={(e) => setFilters({ ...filters, dateFrom: e.target.value })}
            />
          </Grid>
          <Grid size={{ xs: 12, sm: 6 }}>
            <TextField
              label="Период по"
              type="date"
              fullWidth
              size="small"
              slotProps={{ inputLabel: { shrink: true } }}
              value={filters.dateTo ?? ''}
              onChange={(e) => setFilters({ ...filters, dateTo: e.target.value })}
            />
          </Grid>

          <Grid size={{ xs: 12, sm: 6 }}>
            <TextField
              select
              label="Вуз"
              fullWidth
              size="small"
              value={filters.universityId ?? ''}
              onChange={(e) =>
                setFilters({ ...filters, universityId: e.target.value || undefined })
              }
            >
              <MenuItem value="">Все</MenuItem>
              {options?.universities.map((u) => (
                <MenuItem key={u.id} value={u.id}>
                  {u.name}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid size={{ xs: 12, sm: 6 }}>
            <TextField
              select
              label="ИТ-направление"
              fullWidth
              size="small"
              value={filters.directionId ?? ''}
              onChange={(e) =>
                setFilters({ ...filters, directionId: e.target.value || undefined })
              }
            >
              <MenuItem value="">Все</MenuItem>
              {options?.directions.map((d) => (
                <MenuItem key={d.id} value={d.id}>
                  {d.name}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
        </Grid>

        <Divider sx={{ my: 3 }} />

        <Typography variant="subtitle2" gutterBottom>
          Колонки отчёта
        </Typography>
        <FormGroup>
          {columns.map((c) => (
            <FormControlLabel
              key={c.key}
              control={
                <Checkbox
                  size="small"
                  checked={c.selected}
                  onChange={() => toggleColumn(c.key)}
                />
              }
              label={c.label}
            />
          ))}
        </FormGroup>

        <Divider sx={{ my: 3 }} />

        <Stack direction="row" spacing={2} sx={{ alignItems: 'center' }}>
          <TextField
            select
            label="Формат"
            size="small"
            value={format}
            onChange={(e) => setFormat(e.target.value as ReportFormat)}
            sx={{ minWidth: 140 }}
          >
            <MenuItem value="xlsx">XLSX</MenuItem>
            <MenuItem value="xls">XLS</MenuItem>
            <MenuItem value="pdf">PDF</MenuItem>
          </TextField>

          <Button
            variant="contained"
            startIcon={loading ? <CircularProgress size={18} color="inherit" /> : <DownloadIcon />}
            disabled={loading}
            onClick={handleGenerate}
          >
            {loading ? 'Формируется…' : 'Сформировать'}
          </Button>
        </Stack>
      </CardContent>
    </Card>
  )
}
