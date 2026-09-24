import { useState } from 'react'
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Stack,
  TextField,
  MenuItem,
} from '@mui/material'
import { useQuery } from '@tanstack/react-query'
import { catalogApi } from '../api/catalog'
import type { University } from '../types/domain'

export default function ResponsiblesPage() {
  const [side, setSide] = useState<'' | 'school' | 'vuz'>('')

  const { data: all = [], isLoading } = useQuery({
    queryKey: ['responsibles'],
    queryFn: () => catalogApi.getResponsibles(),
  })

  const { data: universitiesData } = useQuery({
    queryKey: ['universities-all'],
    queryFn: () => catalogApi.getUniversities({ pageSize: 100 }),
  })
  const universities: University[] = universitiesData?.items ?? []

  const data = side ? all.filter((r) => r.side === side) : all

  const universityName = (id: string) =>
    universities.find((u) => u.id === id)?.name ?? '—'

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Ответственные</Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Представители ИТ Школы РТК и вузов, ответственные за взаимодействие
      </Typography>

      <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
        <TextField
          select
          label="Сторона"
          value={side}
          onChange={(e) => setSide(e.target.value as '' | 'school' | 'vuz')}
          size="small"
          sx={{ minWidth: 180 }}
        >
          <MenuItem value="">Все</MenuItem>
          <MenuItem value="school">ИТ Школа РТК</MenuItem>
          <MenuItem value="vuz">Вуз</MenuItem>
        </TextField>
      </Stack>

      <Paper>
        <TableContainer>
          <Table sx={{ minWidth: 600 }}>
            <TableHead>
              <TableRow>
                <TableCell>ФИО</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Сторона</TableCell>
                <TableCell>Вуз</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {isLoading ? (
                <TableRow><TableCell colSpan={4}>Загрузка…</TableCell></TableRow>
              ) : (
                data.map((r) => (
                  <TableRow key={r.id} hover>
                    <TableCell>{r.fio}</TableCell>
                    <TableCell>{r.email ?? '—'}</TableCell>
                    <TableCell>
                      <Chip
                        label={r.side === 'school' ? 'ИТ Школа РТК' : 'Вуз'}
                        size="small"
                        color={r.side === 'school' ? 'primary' : 'default'}
                      />
                    </TableCell>
                    <TableCell>{universityName(r.universityId)}</TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  )
}
