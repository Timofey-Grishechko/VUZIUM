import { Box, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material'
import { useQuery } from '@tanstack/react-query'
import { catalogApi } from '../api/catalog'

export default function DirectionsPage() {
  const { data = [], isLoading } = useQuery({
    queryKey: ['directions'],
    queryFn: () => catalogApi.getDirections(),
  })

  return (
    <Box>
      <Typography variant="h4" gutterBottom>ИТ-направления</Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Направления обучения: DevOps, QA, Backend, Frontend и другие
      </Typography>

      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Название</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {isLoading ? (
                <TableRow><TableCell>Загрузка…</TableCell></TableRow>
              ) : (
                data.map((d) => (
                  <TableRow key={d.id} hover>
                    <TableCell>{d.name}</TableCell>
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
