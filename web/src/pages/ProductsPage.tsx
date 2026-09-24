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
} from '@mui/material'
import { useQuery } from '@tanstack/react-query'
import { catalogApi } from '../api/catalog'

export default function ProductsPage() {
  const { data: products = [], isLoading: loadingProducts } = useQuery({
    queryKey: ['products'],
    queryFn: () => catalogApi.getProducts(),
  })
  const { data: vendors = [] } = useQuery({
    queryKey: ['vendors'],
    queryFn: () => catalogApi.getVendors(),
  })
  const { data: directions = [] } = useQuery({
    queryKey: ['directions'],
    queryFn: () => catalogApi.getDirections(),
  })

  const vendorName = (id: string) => vendors.find((v) => v.id === id)?.name ?? '—'
  const directionName = (id: string) => directions.find((d) => d.id === id)?.name ?? '—'

  return (
    <Box>
      <Typography variant="h4" gutterBottom>ИТ-продукты</Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Образовательные программы и продукты по ИТ-направлениям
      </Typography>

      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Название</TableCell>
                <TableCell>Вендор</TableCell>
                <TableCell>Направление</TableCell>
                <TableCell>Описание</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loadingProducts ? (
                <TableRow><TableCell colSpan={4}>Загрузка…</TableCell></TableRow>
              ) : (
                products.map((p) => (
                  <TableRow key={p.id} hover>
                    <TableCell>{p.name}</TableCell>
                    <TableCell>{vendorName(p.vendorId)}</TableCell>
                    <TableCell>
                      <Chip label={directionName(p.directionId)} size="small" color="primary" variant="outlined" />
                    </TableCell>
                    <TableCell>{p.description ?? '—'}</TableCell>
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
