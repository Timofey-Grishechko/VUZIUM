import { Box, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material'
import { useQuery } from '@tanstack/react-query'
import { catalogApi } from '../api/catalog'

export default function VendorsPage() {
  const { data = [], isLoading } = useQuery({
    queryKey: ['vendors'],
    queryFn: () => catalogApi.getVendors(),
  })

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Вендоры</Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Поставщики ИТ-продуктов и образовательных программ
      </Typography>

      <Paper>
        <TableContainer>
          <Table sx={{ minWidth: 400 }}>
            <TableHead>
              <TableRow>
                <TableCell>Название</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {isLoading ? (
                <TableRow><TableCell>Загрузка…</TableCell></TableRow>
              ) : (
                data.map((v) => (
                  <TableRow key={v.id} hover>
                    <TableCell>{v.name}</TableCell>
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
