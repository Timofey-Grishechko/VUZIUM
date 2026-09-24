import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
} from '@mui/material'
import DownloadIcon from '@mui/icons-material/Download'
import type { GeneratedReport } from '../../../api/reports'

interface Props {
  reports: GeneratedReport[]
}

export default function ReportHistory({ reports }: Props) {
  return (
    <Paper elevation={0} sx={{ border: '1px solid', borderColor: 'divider' }}>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Дата</TableCell>
              <TableCell>Файл</TableCell>
              <TableCell>Формат</TableCell>
              <TableCell align="right">Размер</TableCell>
              <TableCell align="right"></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {reports.map((r) => (
              <TableRow key={r.id} hover>
                <TableCell>{r.createdAt}</TableCell>
                <TableCell>{r.filename}</TableCell>
                <TableCell>
                  <Chip label={r.format.toUpperCase()} size="small" variant="outlined" />
                </TableCell>
                <TableCell align="right">{(r.size / 1024).toFixed(0)} КБ</TableCell>
                <TableCell align="right">
                  <IconButton size="small">
                    <DownloadIcon fontSize="small" />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  )
}
