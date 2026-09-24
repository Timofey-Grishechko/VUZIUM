import { useState } from 'react'
import {
  Box,
  Typography,
  TextField,
  MenuItem,
  Stack,
  InputAdornment,
} from '@mui/material'
import SearchIcon from '@mui/icons-material/Search'
import { useNavigate } from 'react-router-dom'

import UniversitiesTable from '../features/catalog/components/UniversitiesTable'
import { useUniversities } from '../features/catalog/hooks/useUniversities'
import { useDebounce } from '../hooks/useDebounce'

export default function UniversitiesPage() {
  const navigate = useNavigate()

  const [search, setSearch] = useState('')
  const [status, setStatus] = useState<'' | 'active' | 'inactive'>('')
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(10)

  const debouncedSearch = useDebounce(search, 300)

  const { data, isLoading } = useUniversities({
    search: debouncedSearch || undefined,
    status: status || undefined,
    page,
    pageSize,
  })

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Вузы
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Каталог высших учебных заведений, участвующих в программах ИТ Школы РТК
      </Typography>

      <Stack
        direction={{ xs: 'column', sm: 'row' }}
        spacing={2}
        sx={{ mb: 3 }}
      >
        <TextField
          placeholder="Поиск по названию"
          value={search}
          onChange={(e) => {
            setSearch(e.target.value)
            setPage(1)
          }}
          size="small"
          sx={{ minWidth: 280 }}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon fontSize="small" />
                </InputAdornment>
              ),
            },
          }}
        />

        <TextField
          select
          label="Статус"
          value={status}
          onChange={(e) => {
            setStatus(e.target.value as '' | 'active' | 'inactive')
            setPage(1)
          }}
          size="small"
          sx={{ minWidth: 180 }}
        >
          <MenuItem value="">Все</MenuItem>
          <MenuItem value="active">Активные</MenuItem>
          <MenuItem value="inactive">Неактивные</MenuItem>
        </TextField>
      </Stack>

      <UniversitiesTable
        items={data?.items ?? []}
        total={data?.total ?? 0}
        page={page}
        pageSize={pageSize}
        loading={isLoading}
        onPageChange={setPage}
        onPageSizeChange={(size) => {
          setPageSize(size)
          setPage(1)
        }}
        onRowClick={(id) => navigate(`/universities/${id}`)}
      />
    </Box>
  )
}
