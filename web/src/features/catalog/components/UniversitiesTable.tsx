import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Chip,
  CircularProgress,
  Box,
  Typography,
} from '@mui/material'

import type { University } from '../../../types/domain'

interface Props {
  items: University[]
  total: number
  page: number
  pageSize: number
  loading: boolean
  onPageChange: (page: number) => void
  onPageSizeChange: (size: number) => void
  onRowClick: (id: string) => void
}

export default function UniversitiesTable({
  items,
  total,
  page,
  pageSize,
  loading,
  onPageChange,
  onPageSizeChange,
  onRowClick,
}: Props) {
  if (loading && items.length === 0) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 6 }}>
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Paper sx={{ width: '100%' }}>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Название</TableCell>
              <TableCell>Регион</TableCell>
              <TableCell>Статус</TableCell>
              <TableCell>Ответственный от вуза</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {items.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} align="center">
                  <Typography color="text.secondary" sx={{ py: 4 }}>
                    Ничего не найдено
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              items.map((u) => (
                <TableRow
                  key={u.id}
                  hover
                  sx={{ cursor: 'pointer' }}
                  onClick={() => onRowClick(u.id)}
                >
                  <TableCell>{u.name}</TableCell>
                  <TableCell>{u.region ?? '—'}</TableCell>
                  <TableCell>
                    <Chip
                      label={u.status === 'active' ? 'Активен' : 'Неактивен'}
                      color={u.status === 'active' ? 'success' : 'default'}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>{u.responsibleFromVuz ?? '—'}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <TablePagination
        component="div"
        count={total}
        page={page - 1}
        onPageChange={(_, newPage) => onPageChange(newPage + 1)}
        rowsPerPage={pageSize}
        onRowsPerPageChange={(e) => onPageSizeChange(Number(e.target.value))}
        rowsPerPageOptions={[5, 10, 25, 50]}
        labelRowsPerPage="Строк на странице"
        labelDisplayedRows={({ from, to, count }) =>
          `${from}–${to} из ${count}`
        }
      />
    </Paper>
  )
}
